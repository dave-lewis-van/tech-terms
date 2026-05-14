---
api:
  file: openapi.yaml
  operationId: get_terms_terms_get
hidden: false
---

## Usage

### List all terms

```bash
curl https://tech-terms-api-production.up.railway.app/terms
```

**Response (`200 OK`):**

```json
[
  {
    "id": 1,
    "term": "SSG",
    "definition": "Static Site Generator.",
    "category": "docs-as-code",
    "see_also": []
  },
  {
    "id": 101,
    "term": "Hydration",
    "definition": "The process of attaching event listeners to static HTML.",
    "category": "frontend",
    "see_also": [105, 202]
  }
]
```

Returns an empty array (`[]`) if no terms exist or no terms match the filters.

### Filter by category

```bash
curl "https://tech-terms-api-production.up.railway.app/terms?category=frontend"
```

Valid `category` values: `frontend`, `backend`, `devops`, `docs-as-code`

### Search by term name

```bash
curl "https://tech-terms-api-production.up.railway.app/terms?search=hydration"
```

The search is case-insensitive and matches against the `term` field only.

### Combine filters

```bash
curl "https://tech-terms-api-production.up.railway.app/terms?category=frontend&search=hydration"
```
