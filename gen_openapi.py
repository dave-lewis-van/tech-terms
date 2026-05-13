import json
import yaml
from main import app

def generate_spec():
    openapi_schema = app.openapi()

    with open("reference/openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)
    print("Successfully generated reference/openapi.yaml")

    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print("Successfully generated openapi.json")

if __name__ == "__main__":
    generate_spec()
