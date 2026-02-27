---
layout: page
title: Search
permalink: /search/
excerpt: "Use the Glittering Spa Blog search tool to find articles by ingredient, concern, or routine step."
faq:
  - question: "How do I search for skincare topics quickly?"
    answer: "Type ingredient names, concerns, or goals into the search field to see matching blog posts instantly."
  - question: "Does search include all published posts?"
    answer: "Yes. Search indexes published posts so you can navigate the full article library faster."
---

<input type="text" id="search-input" placeholder="Search posts...">
<ul id="results-container" class="search-results"></ul>

<script src="https://cdn.jsdelivr.net/npm/simple-jekyll-search@1.11.1/dest/simple-jekyll-search.min.js"></script>
<script>
  SimpleJekyllSearch({
    searchInput: document.getElementById('search-input'),
    resultsContainer: document.getElementById('results-container'),
    json: '/search.json',
    searchResultTemplate: '<li><a href="{url}">{title}</a><span> — {date}</span></li>',
    noResultsText: '<li>No results</li>',
    limit: 20,
    fuzzy: true
  })
</script>

{% include internal-links.html title='Keep exploring' intro='Use these internal links to navigate between blog content and quick tools.' %}
