---
api:
  file: openapi.yaml
  operationId: get_term_terms__id__get
hidden: false
---

## Usage

### Fetch a term by ID

```bash
curl https://tech-terms-api-production.up.railway.app/terms/1
```

**Response (`200 OK`):**

```json
{
  "id": 1,
  "term": "SSG",
  "definition": "Static Site Generator.",
  "category": "docs-as-code",
  "see_also": []
}
```

The `see_also` field contains IDs of related terms. Fetch each ID with another `GET /terms/{id}` call to resolve the full entries.

### Term not found

If no term exists with the given ID, the API returns `404`:

```bash
curl https://tech-terms-api-production.up.railway.app/terms/9999
```

**Response (`404 Not Found`):**

```json
{
  "detail": "Term not found"
}
```

To find a valid ID, use [List Terms](ref:get_terms_terms_get) first.
