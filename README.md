# Glittering Spa Blog (Lean Jekyll Setup)

This repository is intentionally scoped as a **blog-first site** for Glittering Spa.

## What this site should be

A lightweight Jekyll blog used for:
- publishing SEO-friendly posts,
- helping clients discover content via blog index + search,
- keeping maintenance simple.

## Keep only essential pages

- `/` (Home)
- `/blogs/` (Paginated blog listing)
- `/search/` (Client-side search)
- `/about/`
- `/contact/`

## Non-goals

Do **not** expand this repository into a full marketing site with many service pages (e.g., booking, products, gallery, training pages) unless requirements change.

## Reusable prompt for AI assistants

Use this prompt to keep future updates aligned with the intended architecture:

> Refactor and maintain this Jekyll site as a lean company blog (not a full business website).
>
> Goals:
> - Keep only blog-essential pages and navigation.
> - Optimize for publishing, discovery, and readability.
> - Preserve current visual style and dark mode.
>
> Required pages:
> - Home (/)
> - Blogs (/blogs/)
> - Search (/search/)
> - About (/about/)
> - Contact (/contact/)
>
> Tasks:
> 1) Simplify top navigation to only the pages above.
> 2) Keep home layout focused on testimonials + latest 3 posts + clear CTAs.
> 3) Keep paginated blogs index using jekyll-paginate-v2.
> 4) Keep search using simple-jekyll-search + /search.json.
> 5) Keep post layout with metadata, optional cover image, related posts, and JSON-LD article schema.
> 6) Keep theme toggle (localStorage + prefers-color-scheme fallback).
> 7) Keep testimonials feed from Google Sheets with graceful fallback.
> 8) Maintain SEO basics: titles/descriptions, sitemap/feed, canonical URLs.
>
> Non-goals:
> - Do not add booking/services/products/gallery/training pages.
> - Do not convert this repo into a full multi-page business website.
>
> Output:
> - File list and full code changes.
> - Short rationale per change.
> - Run: `bundle install` and `bundle exec jekyll build`.
