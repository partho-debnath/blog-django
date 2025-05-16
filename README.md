# 📝 Django Blog Application

A feature-rich blog application built with Django. This project showcases advanced content management features including tagging, SEO-friendly URLs, full-text and trigram search with PostgreSQL, sitemaps, feeds, comments, and more.

---

## 🚀 Features

- ✅ Post List & Detail Views
- 🏷️ Filter Posts by Tags (using `django-taggit`)
- 💬 Add & Manage Comments
- ✉️ Share Blog Posts via Email
- 🌐 SEO-Friendly URLs (based on slugs and publish date)
- 🔍 Advanced Full-Text Search (PostgreSQL `SearchVector`, `SearchQuery`, `TrigramSimilarity`, `SearchSearchRank`)
- 🧠 Smart Post Recommendations (based on most commented posts)
- 🔖 Custom Template Tags using (`simple_tag`, `inclusion_tag`)
- 🧹 Custom Template Filters
- 🗺️ Sitemap Generation (posts views)
- 📡 RSS/Atom Feed Integration

---

## 🛠️ Tech Stack

- **Framework**: Django
- **Database**: PostgreSQL (required for full-text and trigram search)
- **Search**: `SearchVector`, `TrigramExtension`
- **Tagging**: `django-taggit`
- **Frontend**: HTML5, CSS
- **Others**: Django Sitemaps, Django Feeds

---

## 🔍 Search Implementation

Advanced search is powered by PostgreSQL's:

- `SearchVector` for full-text indexing
- `TrigramSimilarity` for typo-tolerant searching (via `TrigramExtension`)

This enables both relevance-ranked and fuzzy matching search.

---
