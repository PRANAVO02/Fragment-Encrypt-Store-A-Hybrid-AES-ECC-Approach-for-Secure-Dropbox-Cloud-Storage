import json
import os

def load_registry(registry_file="manifests.json"):
    if os.path.exists(registry_file):
        with open(registry_file, "r") as f:
            return json.load(f)
    return {}

def save_registry(registry, registry_file="manifests.json"):
    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=2)
