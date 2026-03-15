from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
import re
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

POSTS_DIR = Path("_posts")
DEFAULT_WEEKS = 26
UNSPLASH_API_BASE = "https://api.unsplash.com"


@dataclass(frozen=True)
class TopicTemplate:
    title: str
    excerpt: str
    tags: list[str]
    keywords: str


TOPIC_ROTATION: list[TopicTemplate] = [
    TopicTemplate(
        title="Weekly skincare plan for Ghana's weather",
        excerpt="Build a practical skincare rhythm for heat, humidity, and dry spells in Ghana.",
        tags=["spa", "skincare", "ghana", "awoshie", "spintex"],
        keywords="spa skincare ghana humidity facial",
    ),
    TopicTemplate(
        title="Medical-esthetic tips for acne and sensitive skin",
        excerpt="Understand safe acne care and when to pair treatment with professional spa support.",
        tags=["spa", "medical advice", "acne", "sensitive skin", "ghana"],
        keywords="acne treatment skincare clinic spa",
    ),
    TopicTemplate(
        title="Body care and product layering that actually works",
        excerpt="Use cleanser, serums, moisturizers, and SPF in the right order for better results.",
        tags=["spa", "products", "body care", "self care", "ghana"],
        keywords="body care spa products routine",
    ),
    TopicTemplate(
        title="Anti-aging support and collagen-friendly spa routines",
        excerpt="Create realistic anti-aging habits with treatment intervals and home maintenance.",
        tags=["spa", "anti aging", "collagen", "facials", "ghana"],
        keywords="anti aging spa facial collagen",
    ),
    TopicTemplate(
        title="Managing hyperpigmentation with professional guidance",
        excerpt="Reduce dark spots with consistent routines, gentle active ingredients, and supervision.",
        tags=["spa", "hyperpigmentation", "medical advice", "products", "ghana"],
        keywords="hyperpigmentation skincare treatment spa",
    ),
    TopicTemplate(
        title="Relaxation, stress relief, and recovery treatments",
        excerpt="Learn massage and wellness combinations that lower stress and support better skin health.",
        tags=["spa", "wellness", "massage", "stress relief", "ghana"],
        keywords="spa wellness massage relaxation",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate 6 months of weekly blog posts promoting the spa in Awoshie and Spintex, "
            "including Unsplash imagery."
        )
    )
    parser.add_argument("--start-date", help="First publish date in YYYY-MM-DD format.")
    parser.add_argument("--weeks", type=int, default=DEFAULT_WEEKS, help="How many weekly posts to generate.")
    parser.add_argument("--unsplash-access-key", help="Unsplash API Access Key. Can also use UNSPLASH_ACCESS_KEY env var.")
    parser.add_argument("--force", action="store_true", help="Overwrite files if they already exist.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files only.")
    return parser.parse_args()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:90].strip("-") or "post"


def resolve_start_date(raw_date: str | None) -> date:
    if raw_date:
        return datetime.strptime(raw_date, "%Y-%m-%d").date()
    return datetime.utcnow().date()


def weekly_dates(start: date, weeks: int) -> list[date]:
    return [start + timedelta(days=7 * index) for index in range(weeks)]


def fetch_unsplash_image_urls(count: int, access_key: str | None, query: str = "spa skincare wellness") -> list[str]:
    if not access_key:
        return [
            f"https://source.unsplash.com/1600x900/?{quote_plus(query)}&sig={index}"
            for index in range(count)
        ]

    endpoint = (
        f"{UNSPLASH_API_BASE}/search/photos?query={quote_plus(query)}&order_by=latest"
        f"&orientation=landscape&per_page={max(count, 30)}"
    )
    request = Request(endpoint, headers={"Authorization": f"Client-ID {access_key}"})

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError):
        return [
            f"https://source.unsplash.com/1600x900/?{quote_plus(query)}&sig={index}"
            for index in range(count)
        ]

    results = payload.get("results", [])
    images = [item.get("urls", {}).get("regular") for item in results]
    clean_images = [url for url in images if url]
    if len(clean_images) < count:
        clean_images.extend(
            f"https://source.unsplash.com/1600x900/?{quote_plus(query)}&sig={index + len(clean_images)}"
            for index in range(count - len(clean_images))
        )
    return clean_images[:count]


def post_body(topic: TopicTemplate) -> str:
    return "\n".join(
        [
            "## Why this topic matters",
            topic.excerpt,
            "",
            "## This week's practical guidance",
            "- Start with a consultation so treatment and product choices match your skin goals.",
            "- Keep routines simple and consistent: cleanse, treat, moisturize, and protect with SPF.",
            "- Track skin response weekly and adjust with professional guidance instead of over-experimenting.",
            "",
            "## Product and treatment spotlight",
            "Ask our team about product pairings and in-spa treatments that fit your skin type, budget, and timeline.",
            "",
            "## Visit us in both locations",
            "Book your appointment at our **Awoshie branch** or **Spintex branch** for personalized support.",
            "",
            "> Medical note: This article is educational and not a substitute for diagnosis or treatment from a licensed medical professional.",
        ]
    )


def build_post_content(
    title: str,
    publish_date: str,
    excerpt: str,
    tags: Iterable[str],
    image_url: str,
    body: str,
) -> str:
    safe_slug = slugify(title)
    tags_text = ", ".join(tags)
    front_matter = [
        "---",
        "layout: post",
        f'title: "{title}"',
        f"date: {publish_date}",
        f"tags: [{tags_text}]",
        "categories: [Spa Advice]",
        f'excerpt: "{excerpt}"',
        f"image: {image_url}",
        'image_alt: "Spa wellness treatment setup"',
        f"permalink: /{safe_slug}/",
        "seo:",
        f'  title: "{title}"',
        f'  description: "{excerpt}"',
        "---",
        "",
    ]
    return "\n".join(front_matter) + body.strip() + "\n"


def generate_calendar(start_date: date, weeks: int, access_key: str | None, force: bool, dry_run: bool) -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    dates = weekly_dates(start_date, weeks)
    image_urls = fetch_unsplash_image_urls(weeks, access_key)

    for index, publish_day in enumerate(dates):
        topic = TOPIC_ROTATION[index % len(TOPIC_ROTATION)]
        week_no = index + 1
        title = f"Week {week_no}: {topic.title}"
        publish_date = publish_day.strftime("%Y-%m-%d")
        filename = f"{publish_date}-{slugify(title)}.md"
        path = POSTS_DIR / filename

        if dry_run:
            print(f"[dry-run] {path}")
            continue

        if path.exists() and not force:
            print(f"Skipped existing post: {path}")
            continue

        content = build_post_content(
            title=title,
            publish_date=publish_date,
            excerpt=topic.excerpt,
            tags=topic.tags,
            image_url=image_urls[index],
            body=post_body(topic),
        )
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path}")
    return 0


def main() -> int:
    args = parse_args()
    start_date = resolve_start_date(args.start_date)
    access_key = args.unsplash_access_key or os.getenv("UNSPLASH_ACCESS_KEY")
    return generate_calendar(start_date, args.weeks, access_key, args.force, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
