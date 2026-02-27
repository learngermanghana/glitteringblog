---
layout: page
title: Blogs
excerpt: "Browse all Glittering Spa Blog articles with pagination for easy discovery."
pagination:
  enabled: true
  per_page: 10
  permalink: '/blogs/page:num/'
faq:
  - question: "How often are new blog posts published?"
    answer: "We publish practical skincare and wellness guides regularly and list the latest posts first."
  - question: "How do I find older blog content?"
    answer: "Use pagination on the blogs page or the search page to locate older posts by keyword."
---

<ul>
{% for post in paginator.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <small>— {{ post.date | date: "%Y-%m-%d" }}</small>
  </li>
{% endfor %}
</ul>

{% if paginator.total_pages > 1 %}
<nav class="pagination" role="navigation">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path | relative_url }}" class="previous">&laquo; Previous</a>
  {% endif %}
  <span class="page-number">Page {{ paginator.page }} of {{ paginator.total_pages }}</span>
  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path | relative_url }}" class="next">Next &raquo;</a>
  {% endif %}
</nav>
{% endif %}

{% include internal-links.html title='Keep exploring' intro='Use these internal links to navigate between blog content and quick tools.' %}
