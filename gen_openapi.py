import os
import yaml
from main import app

# Fields manually maintained in reference/openapi.yaml that gen_openapi.py must not overwrite.
PRESERVED_FIELDS = ["servers", "x-readme"]

def generate_spec():
    openapi_schema = app.openapi()

    # FastAPI generates anyOf:[TermCategory, null] for Optional[TermCategory] query params.
    # This triggers a schemathesis bundling bug. Replace with a direct $ref.
    for param in openapi_schema.get("paths", {}).get("/terms", {}).get("get", {}).get("parameters", []):
        if param.get("name") == "category":
            param["schema"] = {"$ref": "#/components/schemas/TermCategory"}
            break

    # Starlette changed the 422 description between versions; normalise to the RFC 4918 string.
    for path_item in openapi_schema.get("paths", {}).values():
        for operation in path_item.values():
            if isinstance(operation, dict):
                resp = operation.get("responses", {}).get("422", {})
                if resp.get("description") == "Unprocessable Content":
                    resp["description"] = "Unprocessable Entity"

    existing_path = "reference/openapi.yaml"
    if os.path.exists(existing_path):
        with open(existing_path) as f:
            existing = yaml.safe_load(f) or {}
        for field in PRESERVED_FIELDS:
            if field in existing:
                openapi_schema[field] = existing[field]

    with open(existing_path, "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)
    print("Successfully generated reference/openapi.yaml")

if __name__ == "__main__":
    generate_spec()
