---
title: Glossary Management
hidden: false
---

The Glossary Management endpoints let you retrieve and create technical terms in the API's central glossary. Each term has a name, a concise definition, a category (one of `frontend`, `backend`, `devops`, or `docs-as-code`), and optional cross-references to related terms via their IDs.

## Available Operations

| Method | Path | Description |
|---|---|---|
| `GET` | `/terms` | List all terms, with optional `category` and `search` filters |
| `POST` | `/terms` | Register a new term |
| `GET` | `/terms/{id}` | Fetch a specific term by ID |
