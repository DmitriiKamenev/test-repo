def total_price(build: dict) -> int:
    return sum(c.get("price", 0) for c in build.values())
