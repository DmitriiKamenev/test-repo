import math

class PSUCalculator:
    @staticmethod
    def required(build: dict) -> int:
        cpu = build.get("cpu", {}).get("tdp", 0)
        gpu = build.get("gpu", {}).get("tdp", 0)
        return math.ceil((cpu + gpu + 70) * 1.3)
