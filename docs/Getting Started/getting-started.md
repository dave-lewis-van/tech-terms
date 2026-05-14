---
title: Welcome to tech-terms
hidden: false
---

The Technical Terms API is a searchable glossary of terminology used across documentation engineering. Use it to retrieve, search, and manage consistent definitions for frontend, backend, DevOps, and docs-as-code concepts.

**Base URL:** `https://tech-terms-api-production.up.railway.app`

No authentication is required. All endpoints are publicly accessible.

<Cards>
  <Card title="Quick Start" href="ref:getting-started" icon="fa-duotone fa-rocket-launch">Make your first API call in under a minute</Card>

  <Card title="API Reference" href="ref:glossary-management" icon="fa-duotone fa-code-simple">Explore all endpoints and parameters</Card>
</Cards>

<br />

## What You Can Do

<Cards>
  <Card kind="tile" title="List Terms" href="ref:get_terms_terms_get" icon="fa-duotone fa-list">Retrieve all terms, filtered by category or keyword</Card>

  <Card kind="tile" title="Create a Term" href="ref:create_term_terms_post" icon="fa-duotone fa-plus">Add a new term to the glossary</Card>

  <Card kind="tile" title="Fetch by ID" href="ref:get_term_terms__id__get" icon="fa-duotone fa-magnifying-glass">Retrieve a specific term by its numeric ID</Card>
</Cards>

<br />

## Term Categories

Every term belongs to one of four technical domains:

| Category | Description |
|---|---|
| `frontend` | Browser-side technologies: rendering, state, CSS |
| `backend` | Server-side concepts: databases, APIs, services |
| `devops` | Infrastructure, CI/CD, and deployment tooling |
| `docs-as-code` | Documentation workflows, formats, and tooling |
