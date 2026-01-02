import json
from functools import lru_cache

@lru_cache
def load_components(name: str) -> list[dict]:
    with open(f"data/{name}.json", encoding="utf-8") as f:
        return json.load(f)

def get_by_id(component_type: str, cid: str) -> dict:
    return next(
        c for c in load_components(component_type)
        if c["id"] == cid
    )
