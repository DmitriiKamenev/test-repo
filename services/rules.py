from dataclasses import dataclass

@dataclass
class Rule:
    left: str
    op: str
    right: str
    on_fail: list[str]
    message: str
