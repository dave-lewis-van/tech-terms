---
api:
  file: openapi.yaml
  operationId: bulk_import_terms_terms_bulk_post
hidden: false
---

## Usage

### Import multiple terms

```bash
curl -X POST https://tech-terms-api-production.up.railway.app/terms/bulk \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": 11,
      "term": "CI/CD",
      "definition": "Continuous Integration / Continuous Delivery. The practice of automating build, test, and deployment pipelines on every code change.",
      "category": "devops",
      "see_also": []
    },
    {
      "id": 12,
      "term": "Tree Shaking",
      "definition": "The elimination of dead code from a JavaScript bundle at build time.",
      "category": "frontend",
      "see_also": []
    }
  ]'
```

**Response (`207 Multi-Status`):**

```json
[
  { "index": 0, "status": "created", "id": 11 },
  { "index": 1, "status": "created", "id": 12 }
]
```

## Per-item results

Every item in the request produces exactly one result object in the response, keyed by its zero-based `index`.

| Field | Type | Description |
|---|---|---|
| `index` | integer | Zero-based position of the term in the request array. |
| `status` | string | `created` if the term was persisted; `error` if it was rejected. |
| `id` | integer | Present on `created` results. The ID of the new term. |
| `detail` | string | Present on `error` results. Reason the term was rejected. |

Items that fail validation do not block other items in the same batch — valid terms are always persisted.

## Error conditions per item

| Reason | `detail` value |
|---|---|
| Invalid field value (e.g. unknown category) | Pydantic validation message |
| ID already exists in the glossary | `Term with ID {id} already exists.` |
| ID appears more than once in the batch | `Duplicate ID {id} in batch.` |

## Error Response (`400 Bad Request`)

Returned when the request body is an empty array:

```json
{ "detail": "Request body must contain at least one term." }
```
