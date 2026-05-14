---
title: Getting Started
excerpt: Make your first Technical Terms API call in under a minute.
api_config: getting-started
hidden: false
icon: icon-book1
---

## Base URL

All requests go to:

```
https://tech-terms-api-production.up.railway.app
```

## Authentication

No authentication is required. All endpoints are publicly accessible.

## Make Your First Request

Fetch all terms in the glossary:

```bash curl
curl https://tech-terms-api-production.up.railway.app/terms
```

```python python
import requests

response = requests.get("https://tech-terms-api-production.up.railway.app/terms")
print(response.json())
```

```javascript javascript
const response = await fetch("https://tech-terms-api-production.up.railway.app/terms");
const terms = await response.json();
console.log(terms);
```

**Response:**

```json
[
  {
    "id": 1,
    "term": "SSG",
    "definition": "Static Site Generator.",
    "category": "docs-as-code",
    "see_also": []
  }
]
```

## Filter by Category

Use the `category` query parameter to narrow results to a specific domain:

```bash
curl "https://tech-terms-api-production.up.railway.app/terms?category=frontend"
```

Valid values: `frontend`, `backend`, `devops`, `docs-as-code`

## Search by Term Name

Use the `search` query parameter to find terms by keyword:

```bash
curl "https://tech-terms-api-production.up.railway.app/terms?search=hydration"
```

The search matches against term names only.

## Next Steps

- [List Terms](ref:get_terms_terms_get) — full parameter reference for `GET /terms`
- [Create a Term](ref:create_term_terms_post) — add a new entry to the glossary
- [Fetch by ID](ref:get_term_terms__id__get) — retrieve a specific term
