# Technical Terms API

A centralized source of truth for technical terminology used in documentation engineering. The API serves a searchable glossary of terms categorized by domain (frontend, backend, devops, docs-as-code).

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI (Python) |
| Data validation | Pydantic |
| API server | Uvicorn |
| OpenAPI spec | Auto-generated via `gen_openapi.py` |
| API linting | Spectral (`@stoplight/spectral-cli`) |
| Contract testing | Schemathesis |
| Documentation | ReadMe (GitHub sync from `reference/openapi.yaml`) |
| CI/CD | GitHub Actions |

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## Updating the OpenAPI Spec

After modifying `main.py`, regenerate the spec:

```bash
python gen_openapi.py
```

This writes `reference/openapi.yaml`, which is committed and picked up by ReadMe sync and `lint-docs.ts`.

## Linting the Spec

```bash
npx @stoplight/spectral-cli lint reference/openapi.yaml
```

## Running Contract Tests

```bash
uvicorn main:app --host 0.0.0.0 --port 3000 &
schemathesis run ./reference/openapi.yaml --url http://localhost:3000
```

The server runs in the background and persists after you close the terminal. To stop it:

```bash
kill $(lsof -ti :3000)
```

## CI Pipeline

On every push to `v1.0`, GitHub Actions runs:

1. **Generate** — rebuilds `reference/openapi.yaml` from the FastAPI app
2. **Lint** — checks doc quality (`lint-docs.ts`) and validates the spec against Spectral rules
3. **Contract test** — runs Schemathesis against the live API

## API Quick Reference

**Base URL:** `https://tech-terms-api-production.up.railway.app`

**Authentication:** None required.

### Endpoints

| Method | Path | Parameters | Response |
|---|---|---|---|
| `GET` | `/terms` | `category` (enum), `search` (string, matches term name) | `200` array of terms |
| `POST` | `/terms` | JSON body: `GlossaryTerm` | `201` created term; `422` validation error |
| `GET` | `/terms/{id}` | `id` (integer, path) | `200` term; `404` not found |

`GlossaryTerm` fields: `id` (integer, client-supplied), `term` (string), `definition` (string), `category` (enum), `see_also` (integer[], optional).
