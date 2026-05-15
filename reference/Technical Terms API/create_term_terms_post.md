---
api:
  file: openapi.yaml
  operationId: create_term_terms_post
hidden: false
---

## Usage

### Create a term

```bash
curl -X POST https://tech-terms-api-production.up.railway.app/terms \
  -H "Content-Type: application/json" \
  -d '{
    "id": 42,
    "term": "Tree Shaking",
    "definition": "The elimination of dead code from a JavaScript bundle at build time.",
    "category": "frontend",
    "see_also": [101]
  }'
```

**Response (`201 Created`):**

```json
{
  "id": 42,
  "term": "Tree Shaking",
  "definition": "The elimination of dead code from a JavaScript bundle at build time.",
  "category": "frontend",
  "see_also": [101]
}
```

## Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | integer | Yes | A unique numeric identifier you supply. See note below. |
| `term` | string | Yes | The canonical name of the technical concept. |
| `definition` | string | Yes | A concise, technical explanation of the term. |
| `category` | string | Yes | One of: `frontend`, `backend`, `devops`, `docs-as-code` |
| `see_also` | integer[] | No | IDs of related glossary entries. Relationships are one-way. |

**Note on `id`:** IDs are client-supplied. The API does not auto-increment or enforce uniqueness — submitting a duplicate ID will create a duplicate entry. Auto-increment IDs are planned for a future release.

**Note on persistence:** Created terms are saved to a `terms.json` file on the server and survive restarts. However, the production server runs on Railway, which uses an ephemeral filesystem — terms will be lost if the server is redeployed.

## Error Response (`422 Unprocessable Entity`)

Returned when the request body is missing required fields or contains invalid values:

```json
{
  "detail": [
    {
      "loc": ["body", "category"],
      "msg": "value is not a valid enumeration member; permitted: 'frontend', 'backend', 'devops', 'docs-as-code'",
      "type": "type_error.enum",
      "input": "cloud"
    }
  ]
}
```
