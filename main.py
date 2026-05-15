import json
from pathlib import Path as FilePath
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import List, Optional

app = FastAPI(
    title="Technical Terms API",
    description=(
        "A searchable glossary of technical terminology used in documentation engineering. "
        "Terms are organized by domain — frontend, backend, devops, and docs-as-code — and "
        "can be retrieved, filtered, and created via this API.\n\n"
        "**Base URL:** `https://tech-terms-api-production.up.railway.app`\n\n"
        "**Authentication:** None required. All endpoints are publicly accessible."
    ),
    version="1.0.0",
    contact={"url": "https://github.com/dave-lewis-van/tech-terms/issues"},
    openapi_tags=[{"name": "Terms", "description": "Retrieve and create technical glossary terms."}],
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS (The 'Schema') ---

class TermCategory(str, Enum):
    frontend = "frontend"
    backend = "backend"
    devops = "devops"
    docs_as_code = "docs-as-code"

class GlossaryTerm(BaseModel):
    id: int = Field(..., example=101)
    term: str = Field(..., example="Hydration", description="The canonical name of the technical concept.")
    definition: str = Field(..., example="The process of attaching event listeners to static HTML.", description="A concise, technical explanation of the term.")
    category: TermCategory = Field(..., example="frontend")
    see_also: Optional[List[int]] = Field(None, example=[105, 202], description="IDs of related glossary entries.")

    @validator('id', pre=True)
    def id_no_booleans(cls, v):
        if isinstance(v, bool):
            raise ValueError('id must be an integer, not a boolean')
        return v

    @validator('see_also', each_item=True, pre=True)
    def see_also_no_booleans(cls, v):
        if isinstance(v, bool):
            raise ValueError('see_also items must be integers')
        return v

# --- DATABASE ---

DATA_FILE = FilePath("terms.json")
_default = [{"id": 1, "term": "SSG", "definition": "Static Site Generator.", "category": "docs-as-code", "see_also": []}]

def _load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    DATA_FILE.write_text(json.dumps(_default, indent=2))
    return _default

def _save(db):
    DATA_FILE.write_text(json.dumps(db, indent=2))

glossary_db = _load()

# --- ENDPOINTS ---

@app.get("/terms", response_model=List[GlossaryTerm], tags=["Terms"], responses={
    200: {"content": {"application/json": {"example": [
        {"id": 1, "term": "SSG", "definition": "Static Site Generator.", "category": "docs-as-code", "see_also": []},
        {"id": 101, "term": "Hydration", "definition": "The process of attaching event listeners to static HTML.", "category": "frontend", "see_also": [105, 202]},
    ]}}},
})
async def get_terms(
    category: Optional[TermCategory] = Query(None, description="Filter terms by technical domain."),
    search: Optional[str] = Query(None, description="Search term names by keyword (case-insensitive).")
):
    """Retrieve a list of technical terms with optional filtering."""
    results = glossary_db
    if category:
        results = [t for t in results if t["category"] == category]
    if search:
        results = [t for t in results if search.lower() in t["term"].lower()]
    return results

@app.post("/terms", response_model=GlossaryTerm, status_code=201, tags=["Terms"], responses={
    201: {"content": {"application/json": {"example":
        {"id": 42, "term": "Tree Shaking", "definition": "The elimination of dead code from a JavaScript bundle at build time.", "category": "frontend", "see_also": [101]},
    }}},
    422: {"content": {"application/json": {"example":
        {"detail": [{"loc": ["body", "category"], "msg": "value is not a valid enumeration member; permitted: 'frontend', 'backend', 'devops', 'docs-as-code'", "type": "type_error.enum", "input": "cloud"}]},
    }}},
})
async def create_term(term: GlossaryTerm):
    """Register a new technical term in the glossary."""
    glossary_db.append(term.dict())
    _save(glossary_db)
    return term

@app.get("/terms/{id}", response_model=GlossaryTerm, tags=["Terms"], responses={
    200: {"content": {"application/json": {"example":
        {"id": 101, "term": "Hydration", "definition": "The process of attaching event listeners to static HTML.", "category": "frontend", "see_also": [105, 202]},
    }}},
    404: {"description": "Term not found", "content": {"application/json": {"example": {"detail": "Term not found"}}}},
})
async def get_term(id: int = Path(..., description="The unique numeric ID of the glossary term.")):
    """Fetch a specific term by its ID."""
    term = next((t for t in glossary_db if t["id"] == id), None)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term