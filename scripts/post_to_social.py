from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib import parse, request


def parse_front_matter(markdown_text: str) -> dict[str, str]:
    if not markdown_text.startswith("---\n"):
        raise ValueError("Post does not start with YAML front matter.")

    try:
        _, fm_block, body = markdown_text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("Could not parse front matter block.") from exc

    data: dict[str, str] = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    data["_body"] = body.strip()
    return data


def slug_from_filename(path: Path) -> str:
    name = path.stem
    return re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)


def post_url(site_url: str, post_path: Path) -> str:
    return f"{site_url.rstrip('/')}/{slug_from_filename(post_path)}/"


def excerpt_from_body(body: str, max_len: int = 220) -> str:
    cleaned = re.sub(r"[#*_`>\-]", "", body)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 1].rstrip() + "…"


def post_json(url: str, payload: dict, headers: dict[str, str]) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Content-Type", "application/json")

    with request.urlopen(req) as resp:  # noqa: S310 - trusted URLs from APIs
        return resp.status, resp.read().decode("utf-8")


def publish_linkedin(text: str, article_url: str, dry_run: bool) -> None:
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")
    if not token or not person_urn:
        print("[linkedin] Skipped: missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN")
        return

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": f"{text}\n\nRead more: {article_url}"},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    if dry_run:
        print("[linkedin] Dry run: would publish post")
        return

    status, body = post_json(
        "https://api.linkedin.com/v2/ugcPosts",
        payload,
        {"Authorization": f"Bearer {token}", "X-Restli-Protocol-Version": "2.0.0"},
    )
    print(f"[linkedin] Published (status={status}): {body[:160]}")


def publish_medium(title: str, content_markdown: str, article_url: str, dry_run: bool) -> None:
    token = os.getenv("MEDIUM_TOKEN")
    user_id = os.getenv("MEDIUM_USER_ID")
    if not token or not user_id:
        print("[medium] Skipped: missing MEDIUM_TOKEN or MEDIUM_USER_ID")
        return

    content = f"{content_markdown}\n\nOriginally published: [{article_url}]({article_url})"
    payload = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "publishStatus": "public",
    }
    if dry_run:
        print("[medium] Dry run: would publish article")
        return

    status, body = post_json(
        f"https://api.medium.com/v1/users/{parse.quote(user_id)}/posts",
        payload,
        {"Authorization": f"Bearer {token}"},
    )
    print(f"[medium] Published (status={status}): {body[:160]}")


def publish_instagram(caption: str, article_url: str, image_url: str | None, dry_run: bool) -> None:
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    account_id = os.getenv("INSTAGRAM_ACCOUNT_ID")
    if not token or not account_id:
        print("[instagram] Skipped: missing INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID")
        return
    if not image_url:
        print("[instagram] Skipped: post has no `image:` URL in front matter")
        return

    final_caption = f"{caption}\n\nRead more: {article_url}"
    create_url = f"https://graph.facebook.com/v20.0/{account_id}/media"
    publish_url = f"https://graph.facebook.com/v20.0/{account_id}/media_publish"

    if dry_run:
        print("[instagram] Dry run: would create media container + publish")
        return

    container_payload = {
        "image_url": image_url,
        "caption": final_caption,
        "access_token": token,
    }
    status, body = post_json(create_url, container_payload, {})
    data = json.loads(body)
    creation_id = data.get("id")
    if not creation_id:
        raise RuntimeError(f"[instagram] Failed creating media container (status={status}): {body}")

    status2, body2 = post_json(publish_url, {"creation_id": creation_id, "access_token": token}, {})
    print(f"[instagram] Published (status={status2}): {body2[:160]}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish a blog post to social channels.")
    parser.add_argument("--post", required=True, help="Path to post markdown file in _posts/.")
    parser.add_argument("--site-url", default=os.getenv("SITE_URL", "https://falowen.com"))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    post_path = Path(args.post)
    if not post_path.exists():
        raise FileNotFoundError(f"Post not found: {post_path}")

    fm = parse_front_matter(post_path.read_text(encoding="utf-8"))
    title = fm.get("title", post_path.stem)
    body = fm.get("_body", "")
    excerpt = fm.get("excerpt") or excerpt_from_body(body)
    image_url = fm.get("image")

    url = post_url(args.site_url, post_path)

    publish_linkedin(f"{title}\n\n{excerpt}", url, args.dry_run)
    publish_instagram(f"{title}\n\n{excerpt}", url, image_url, args.dry_run)
    publish_medium(title, body, url, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
