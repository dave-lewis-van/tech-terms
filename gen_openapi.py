import json
import yaml
from main import app

def generate_spec():
    openapi_schema = app.openapi()

    # FastAPI generates anyOf:[TermCategory, null] for Optional[TermCategory] query params.
    # This triggers a schemathesis bundling bug. Replace with a direct $ref.
    for param in openapi_schema.get("paths", {}).get("/terms", {}).get("get", {}).get("parameters", []):
        if param.get("name") == "category":
            param["schema"] = {"$ref": "#/components/schemas/TermCategory"}
            break

    with open("reference/openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)
    print("Successfully generated reference/openapi.yaml")

    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("Successfully generated openapi.json")

if __name__ == "__main__":
    generate_spec()
