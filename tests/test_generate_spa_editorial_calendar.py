import unittest
from datetime import date

from scripts.generate_spa_editorial_calendar import (
    TopicTemplate,
    build_post_content,
    fetch_unsplash_image_urls,
    post_body,
    weekly_dates,
)


class SpaCalendarGeneratorTests(unittest.TestCase):
    def test_weekly_dates_returns_seven_day_intervals(self) -> None:
        result = weekly_dates(date(2026, 1, 1), 3)
        self.assertEqual(result, [date(2026, 1, 1), date(2026, 1, 8), date(2026, 1, 15)])

    def test_post_body_promotes_both_branches_and_has_medical_note(self) -> None:
        topic = TopicTemplate(
            title="Test",
            excerpt="excerpt",
            tags=["spa"],
            keywords="spa",
        )
        body = post_body(topic)

        self.assertIn("Awoshie branch", body)
        self.assertIn("Spintex branch", body)
        self.assertIn("not a substitute", body)

    def test_build_post_content_sets_spa_category(self) -> None:
        md = build_post_content(
            title="Week 1: Test",
            publish_date="2026-01-01",
            excerpt="hello",
            tags=["spa", "ghana"],
            image_url="https://example.com/image.jpg",
            body="Body",
        )

        self.assertIn("categories: [Spa Advice]", md)
        self.assertIn("image: https://example.com/image.jpg", md)

    def test_fetch_unsplash_fallback_without_key(self) -> None:
        images = fetch_unsplash_image_urls(2, None, query="spa wellness")

        self.assertEqual(len(images), 2)
        self.assertIn("source.unsplash.com", images[0])


if __name__ == "__main__":
    unittest.main()
