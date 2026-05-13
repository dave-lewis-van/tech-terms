from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

app = FastAPI(
    title="Technical Terms API",
    description="A centralized programmatic 'Source of Truth' for technical terminology used in documentation engineering.",
    version="1.0.0",
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

# --- MOCK DATABASE ---

glossary_db = [
    {"id": 1, "term": "SSG", "definition": "Static Site Generator.", "category": "docs-as-code", "see_also": []},
]

# --- ENDPOINTS ---

@app.get("/terms", response_model=List[GlossaryTerm], tags=["Glossary Management"])
async def get_terms(
    category: Optional[TermCategory] = Query(None, description="Filter terms by technical domain."),
    search: Optional[str] = Query(None, description="Search terms and definitions by keyword.")
):
    """Retrieve a list of technical terms with optional filtering."""
    results = glossary_db
    if category:
        results = [t for t in results if t["category"] == category]
    if search:
        results = [t for t in results if search.lower() in t["term"].lower()]
    return results

@app.post("/terms", response_model=GlossaryTerm, status_code=201, tags=["Glossary Management"])
async def create_term(term: GlossaryTerm):
    """Register a new technical term in the glossary."""
    glossary_db.append(term.dict())
    return term

@app.get("/terms/{id}", response_model=GlossaryTerm, tags=["Glossary Management"])
async def get_term(id: int = Path(..., description="The unique numeric ID of the glossary term.")):
    """Fetch a specific term by its ID."""
    term = next((t for t in glossary_db if t["id"] == id), None)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term