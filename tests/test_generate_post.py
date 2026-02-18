import unittest

from scripts.generate_post import build_post


class BuildPostTests(unittest.TestCase):
    def test_build_post_uses_category_argument(self) -> None:
        md = build_post(
            title="Test title",
            excerpt="Test excerpt",
            category="Guides",
            tags=["falowen", "german"],
            image_url="https://example.com/image.jpg",
            image_alt="alt text",
            permalink_slug="test-title",
            seo_title="SEO title",
            seo_description="SEO description",
            body="Body text",
            publish_date="2026-02-16",
        )

        self.assertIn("categories: [Guides]", md)

    def test_build_post_uses_explicit_parameters_for_front_matter(self) -> None:
        md = build_post(
            title="A title",
            excerpt="Custom excerpt",
            category="News",
            tags=["a", "b"],
            image_url="https://example.com/custom-image.jpg",
            image_alt="custom alt",
            permalink_slug="custom-slug",
            seo_title="Custom SEO title",
            seo_description="Custom SEO description",
            body="  Main body text  ",
            publish_date="2026-02-16",
        )

        self.assertIn('excerpt: "Custom excerpt"', md)
        self.assertIn("image: https://example.com/custom-image.jpg", md)
        self.assertIn('image_alt: "custom alt"', md)
        self.assertIn("permalink: /custom-slug/", md)
        self.assertIn('  title: "Custom SEO title"', md)
        self.assertIn('  description: "Custom SEO description"', md)
        self.assertTrue(md.endswith("Main body text\n"))


if __name__ == "__main__":
    unittest.main()
