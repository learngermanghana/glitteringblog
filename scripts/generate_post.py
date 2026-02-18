from __future__ import annotations

import argparse
from datetime import datetime, date
from pathlib import Path
import re

POSTS_DIR = Path("_posts")

GERMAN_CHAR_MAP = {
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    for src, target in GERMAN_CHAR_MAP.items():
        text = text.replace(src, target)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return (text[:90].strip("-") or "post")


def build_post(
    title: str,
    excerpt: str,
    category: str,
    tags: list[str],
    image_url: str,
    image_alt: str,
    permalink_slug: str,
    seo_title: str,
    seo_description: str,
    body: str,
    publish_date: str,
) -> str:
    tag_string = ", ".join(tags)

    fm = [
        "---",
        "layout: post",
        f'title: "{title}"',
        f"date: {publish_date}",
        f"tags: [{tag_string}]",
        f"categories: [{category}]",
        f'excerpt: "{excerpt}"',
        f"image: {image_url}",
        f'image_alt: "{image_alt}"',
        f"permalink: /{permalink_slug}/",
        "seo:",
        f'  title: "{seo_title}"',
        f'  description: "{seo_description}"',
        "---",
        "",
    ]
    return "\n".join(fm) + body.strip() + "\n"


def build_structured_body(
    intro_heading: str,
    intro_lines: list[str],
    sections: list[dict],
    comparison_rows: list[tuple[str, str, str, str]],
    mistakes: list[tuple[str, str]],
    practice_items: list[str],
    final_lines: list[str],
) -> str:
    lines = [f"## {intro_heading}"]
    lines.extend(intro_lines)
    lines.append("")
    lines.append("---")
    lines.append("")

    for idx, section in enumerate(sections, 1):
        lines.append(f"## {idx}. **{section['title']}**")
        lines.extend(section["explanation"])
        lines.append("")
        lines.append("**Examples**")
        for example in section["examples"]:
            lines.append(f"- *{example}*")
        lines.append("")
        lines.append(f"**Tone:** {section['tone']}")
        lines.append(f"**Use it when:** {section['usage']}")
        if section.get("warning"):
            lines.append("")
            lines.append("**Be careful:**")
            lines.extend(section["warning"])
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Quick comparison")
    lines.append("")
    lines.append("| Expression | Meaning | Politeness | Typical use |")
    lines.append("|------------|---------|------------|-------------|")
    for expr, meaning, politeness, use_case in comparison_rows:
        lines.append(f"| **{expr}** | {meaning} | {politeness} | {use_case} |")

    lines += ["", "---", "", "## Typical mistakes learners make", ""]
    for wrong, correct in mistakes:
        lines.append(f"✗ *{wrong}*")
        lines.append(f"✓ *{correct}*")
        lines.append("")

    lines += ["---", "", "## How to practice in Falowen", ""]
    for item in practice_items:
        lines.append(f"- {item}")

    lines += ["", "---", "", "## Final thoughts"]
    lines.extend(final_lines)
    lines += ["", "👉 Practice now at **falowen.app**"]
    return "\n".join(lines)


def a1_vocab_body() -> str:
    return build_structured_body(
        intro_heading="Why daily vocabulary matters",
        intro_lines=[
            "When beginners learn isolated words, they forget quickly.",
            "When you learn words with **context + mini actions**, they stay in memory and become usable in speaking.",
        ],
        sections=[
            {
                "title": "Alltag nouns and verbs",
                "explanation": ["These words help you describe a full day with simple A1 sentence patterns."],
                "examples": [
                    "Ich frühstücke um 7 Uhr.",
                    "Ich arbeite von Montag bis Freitag.",
                    "Am Abend koche ich Nudeln.",
                ],
                "tone": "neutral, daily conversation",
                "usage": "describing routines at school, work, and home",
            },
            {
                "title": "Time connectors for routine",
                "explanation": ["Use small connectors to sound natural, even with short sentences."],
                "examples": [
                    "Zuerst frühstücke ich, dann gehe ich zur Arbeit.",
                    "Am Abend lerne ich Deutsch und schlafe um 22 Uhr.",
                ],
                "tone": "simple and clear",
                "usage": "building mini paragraphs, not just single lines",
            },
        ],
        comparison_rows=[
            ("frühstücken", "to have breakfast", "neutral", "morning routine"),
            ("arbeiten", "to work", "neutral", "work/school life"),
            ("spazieren gehen", "to go for a walk", "friendly", "free-time talk"),
        ],
        mistakes=[
            ("Ich lernen jeden Tag Deutsch.", "Ich lerne jeden Tag Deutsch."),
            ("Ich gehe einkaufen im Supermarkt.", "Ich kaufe im Supermarkt ein."),
        ],
        practice_items=[
            "Topic Coach: Describe your day in 6 lines using at least 5 routine verbs.",
            "Sentence Trainer: Alternate present tense subjects (ich / wir / sie).",
            "Writing Trainer: Write a mini diary entry for one weekday.",
        ],
        final_lines=[
            "Small A1 words become powerful when you reuse them in meaningful routines.",
            "Practice this weekly and your fluency grows faster than memorizing random lists.",
        ],
    )


def a2_connectors_body() -> str:
    return build_structured_body(
        intro_heading="Why connectors change your writing quality",
        intro_lines=[
            "A2 learners often know grammar but still write short, disconnected sentences.",
            "Connectors create **flow**, show **logic**, and help you score higher in letters and short essays.",
        ],
        sections=[
            {
                "title": "Cause and effect connectors",
                "explanation": ["Use these to explain reasons and consequences clearly."],
                "examples": [
                    "Ich bleibe zu Hause, weil ich müde bin.",
                    "Ich war krank, deshalb bin ich nicht gekommen.",
                    "Es regnet, trotzdem gehe ich spazieren.",
                ],
                "tone": "structured, explanatory",
                "usage": "emails, excuses, and planning messages",
            },
            {
                "title": "Sequence and contrast connectors",
                "explanation": ["These make your text feel organized and balanced."],
                "examples": [
                    "Zuerst lerne ich Vokabeln, dann übe ich Schreiben.",
                    "Ich möchte kommen, aber ich habe keine Zeit.",
                    "Ich lerne nicht nur Wörter, sondern auch Grammatik.",
                ],
                "tone": "clear and coherent",
                "usage": "exam tasks, invitations, and short opinions",
            },
        ],
        comparison_rows=[
            ("weil", "because", "neutral", "giving reasons"),
            ("deshalb", "therefore", "neutral", "showing result"),
            ("trotzdem", "nevertheless", "slightly advanced", "contrast"),
        ],
        mistakes=[
            ("Ich lerne jeden Tag. Deshalb ich mache Fortschritte.", "Ich lerne jeden Tag. Deshalb mache ich Fortschritte."),
            ("Ich bleibe zu Hause, deshalb ich bin müde.", "Ich bleibe zu Hause, weil ich müde bin."),
        ],
        practice_items=[
            "Topic Coach: Explain one problem and one solution using weil/deshalb/trotzdem.",
            "Sentence Trainer: Combine two short lines into one logical sentence.",
            "Writing Trainer: Write an A2 letter with at least six connectors.",
        ],
        final_lines=[
            "Connectors are the bridge between grammar knowledge and natural communication.",
            "If your text has logic and flow, your German immediately sounds more mature.",
        ],
    )


def b1_opinion_body() -> str:
    return build_structured_body(
        intro_heading="Why B1 opinions need structure",
        intro_lines=[
            "At B1 level, the goal is not only to give an opinion but to support it clearly.",
            "With the right phrases, your writing sounds balanced, thoughtful, and exam-ready.",
        ],
        sections=[
            {
                "title": "Core opinion starters",
                "explanation": ["These phrases make your stance clear from the beginning."],
                "examples": [
                    "Meiner Meinung nach ist Online-Lernen sehr praktisch.",
                    "Ich bin der Ansicht, dass tägliche Übung wichtig ist.",
                ],
                "tone": "balanced and clear",
                "usage": "introductions and opening argument",
            },
            {
                "title": "Balancing arguments and conclusions",
                "explanation": ["Use contrast and conclusion phrases to show mature reasoning."],
                "examples": [
                    "Einerseits spart man Zeit, andererseits fehlt der Kontakt.",
                    "Zum Schluss möchte ich sagen, dass Disziplin entscheidend ist.",
                ],
                "tone": "reasoned and organized",
                "usage": "middle and final paragraph",
            },
        ],
        comparison_rows=[
            ("Meiner Meinung nach", "in my opinion", "neutral polite", "opening view"),
            ("Einerseits … andererseits", "on one hand … on the other", "formal", "balanced argument"),
            ("Zum Schluss", "in conclusion", "neutral", "closing statement"),
        ],
        mistakes=[
            ("Ich finde das gut. Und ich finde das schlecht.", "Einerseits ist es praktisch, andererseits gibt es Nachteile."),
            ("Ich denke, dass. Es ist wichtig.", "Ich denke, dass tägliche Übung wichtig ist."),
        ],
        practice_items=[
            "Topic Coach: Defend and challenge one idea in the same response.",
            "Sentence Trainer: Rewrite direct opinions into nuanced opinions.",
            "Writing Trainer: Write 120–150 words with intro, contrast, and conclusion.",
        ],
        final_lines=[
            "Strong B1 writing is a combination of opinion + support + structure.",
            "When your argument is balanced, your voice sounds confident and credible.",
        ],
    )


def b2_discussion_body() -> str:
    return build_structured_body(
        intro_heading="Why B2 discussion writing requires precision",
        intro_lines=[
            "At B2 level, ideas must be nuanced, not just correct.",
            "You need structured arguments, clear transitions, and evidence-based claims.",
        ],
        sections=[
            {
                "title": "Framing a modern debate",
                "explanation": ["Use debate framing to show analytical thinking from the first paragraph."],
                "examples": [
                    "Es lässt sich feststellen, dass KI Lernprozesse deutlich beschleunigen kann.",
                    "Nicht zu unterschätzen ist, dass Datenschutzrisiken weiterhin bestehen.",
                ],
                "tone": "analytical",
                "usage": "introduction and thesis framing",
            },
            {
                "title": "Balancing advantages and risks",
                "explanation": ["High-scoring B2 texts compare sides before concluding."],
                "examples": [
                    "Demgegenüber steht jedoch, dass automatisierte Inhalte nicht immer zuverlässig sind.",
                    "Zusammenfassend kann man sagen, dass KI sinnvoll ist, wenn klare Regeln gelten.",
                ],
                "tone": "formal and nuanced",
                "usage": "argument body and final evaluation",
            },
        ],
        comparison_rows=[
            ("Es lässt sich feststellen, dass", "it can be observed that", "formal", "objective claim"),
            ("Demgegenüber steht jedoch, dass", "in contrast, however", "formal", "counter-argument"),
            ("Zusammenfassend kann man sagen, dass", "to summarize", "formal", "conclusion"),
        ],
        mistakes=[
            ("KI ist gut. KI ist schlecht.", "KI bietet Effizienzvorteile, birgt jedoch erhebliche Datenschutzrisiken."),
            ("Ich finde, dass KI ist gut.", "Ich bin der Ansicht, dass KI in klaren Grenzen sinnvoll ist."),
        ],
        practice_items=[
            "Topic Coach: Defend one policy and challenge it with one risk.",
            "Sentence Trainer: Turn simple opinions into formal B2 structures.",
            "Writing Trainer: Write 180–220 words with at least four advanced connectors.",
        ],
        final_lines=[
            "Excellent B2 texts show control of language and control of argument logic.",
            "Train with realistic prompts and your written German will sound truly advanced.",
        ],
    )


# ---------- Rotation Logic ----------

def week_index_utc() -> int:
    return date.today().isocalendar().week

def get_topic_for_week(week_index: int) -> dict:
    topics = [
        {
            "title": "A1: Daily Vocabulary with Examples and Mini Routines",
            "excerpt": "A1 vocabulary with context, common mistakes, and practical routines for daily speaking.",
            "category": "Guides",
            "tags": ["falowen", "german", "a1", "vocabulary", "daily routines"],
            "image": "https://raw.githubusercontent.com/learngermanghana/falowen-blog/main/photos/pexels-polina-kovaleva-8362564.jpg",
            "image_alt": "Student writing a German daily routine plan at a study desk",
            "seo_title": "A1 German Daily Vocabulary Guide – Examples and Mini Routines",
            "seo_description": "Learn useful A1 German vocabulary for daily routines with examples, mistakes to avoid, and Falowen practice tasks.",
            "permalink_slug": "a1-daily-vocabulary-guide",
            "body": a1_vocab_body(),
        },
        {
            "title": "A2: Use Connectors Correctly to Write with Better Logic",
            "excerpt": "Learn A2 connectors with deeper examples, common errors, and practical writing drills.",
            "category": "Guides",
            "tags": ["falowen", "german", "a2", "writing", "connectors"],
            "image": "https://raw.githubusercontent.com/learngermanghana/falowen-blog/main/photos/pexels-joshuamckn-1139317.jpg",
            "image_alt": "German learner reviewing connector notes for A2 writing",
            "seo_title": "A2 German Connectors Guide – Write with Better Flow",
            "seo_description": "Master A2 connectors like weil, deshalb, trotzdem, and aber with examples, mistakes, and practice ideas.",
            "permalink_slug": "a2-german-connectors-writing-guide",
            "body": a2_connectors_body(),
        },
        {
            "title": "B1: Express Opinions with Structure – Phrases, Examples, Mistakes",
            "excerpt": "B1 opinion-writing guide with phrases, argument structure, and exam-focused practice.",
            "category": "Guides",
            "tags": ["falowen", "german", "b1", "writing", "opinion"],
            "image": "https://raw.githubusercontent.com/learngermanghana/falowen-blog/main/photos/pexels-rdne-8499492.jpg",
            "image_alt": "Learner drafting a structured B1 German opinion text",
            "seo_title": "B1 German Opinion Writing – Structure and Useful Phrases",
            "seo_description": "Improve B1 German writing with opinion starters, contrast phrases, common mistakes, and practical drills.",
            "permalink_slug": "b1-opinion-writing-structure-guide",
            "body": b1_opinion_body(),
        },
        {
            "title": "B2: Write Discussions About AI with Precise Arguments",
            "excerpt": "B2 discussion-writing blueprint with advanced structures, balanced arguments, and exam practice.",
            "category": "Guides",
            "tags": ["falowen", "german", "b2", "discussion", "exam writing"],
            "image": "https://raw.githubusercontent.com/learngermanghana/falowen-blog/main/photos/pexels-prince-beguin-81839921-10334158.jpg",
            "image_alt": "Student and laptop symbolizing advanced B2 discussion writing on AI",
            "seo_title": "B2 German Discussion Writing – AI Topic Structure Guide",
            "seo_description": "Write stronger B2 discussion texts with formal phrases, comparison logic, and practical Falowen exercises.",
            "permalink_slug": "b2-discussion-writing-ai-guide",
            "body": b2_discussion_body(),
        },
    ]
    idx = (week_index - 1) % len(topics)
    return topics[idx]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one weekly blog post in _posts/.")
    parser.add_argument(
        "--date",
        help="Publishing date in YYYY-MM-DD format (default: current UTC date).",
    )
    parser.add_argument(
        "--week-index",
        type=int,
        help="ISO week index override for topic rotation (default: current ISO week).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Create a file even if one with the same name already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned filename/topic and exit without writing files.",
    )
    return parser.parse_args()


def resolve_publish_date(raw_date: str | None) -> str:
    if raw_date is None:
        return datetime.utcnow().strftime("%Y-%m-%d")

    # Validate strict YYYY-MM-DD input.
    datetime.strptime(raw_date, "%Y-%m-%d")
    return raw_date


def post_already_contains_title(title: str) -> bool:
    escaped_title = re.escape(f'title: "{title}"')
    title_pattern = re.compile(rf"^{escaped_title}$", re.MULTILINE)
    for post_file in POSTS_DIR.glob("*.md"):
        if title_pattern.search(post_file.read_text(encoding="utf-8")):
            return True
    return False

def main() -> int:
    args = parse_args()
    POSTS_DIR.mkdir(parents=True, exist_ok=True)

    selected_week_index = args.week_index or week_index_utc()
    topic = get_topic_for_week(selected_week_index)

    publish_date = resolve_publish_date(args.date)
    slug = slugify(topic["title"])
    filename = f"{publish_date}-{slug}.md"
    path = POSTS_DIR / filename

    if args.dry_run:
        print(f"[dry-run] Week index: {selected_week_index}")
        print(f"[dry-run] Topic: {topic['title']}")
        print(f"[dry-run] Target file: {path}")
        return 0

    # If rerun same day (or same topic), do nothing.
    if path.exists() and not args.force:
        print(f"Post already exists: {path}")
        return 0

    if post_already_contains_title(topic["title"]) and not args.force:
        print(f"Post with this title already exists: {topic['title']}")
        return 0

    md = build_post(
        title=topic["title"],
        excerpt=topic["excerpt"],
        category=topic["category"],
        tags=topic["tags"],
        image_url=topic["image"],
        image_alt=topic["image_alt"],
        permalink_slug=topic["permalink_slug"],
        seo_title=topic["seo_title"],
        seo_description=topic["seo_description"],
        body=topic["body"],
        publish_date=publish_date,
    )

    path.write_text(md, encoding="utf-8")
    print(f"Created: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
