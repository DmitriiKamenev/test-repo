from services.json_loader import load_components
from services.rule_engine import is_component_compatible

def get_available_components(component_type: str, build: dict):
    components = load_components(component_type)
    return [
        c for c in components
        if is_component_compatible(build, c)
    ]
