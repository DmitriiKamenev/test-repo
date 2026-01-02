from services.rules import Rule
from services.psu_calculator import PSUCalculator
from copy import deepcopy

OPS = {
    "==": lambda a, b: a == b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}

RULES = [
    Rule(
        left="cpu.socket",
        op="==",
        right="motherboard.socket",
        on_fail=["motherboard", "ram"],
        message="🧠 CPU несовместим с материнской платой"
    ),
    Rule(
        left="ram.memory_type",
        op="==",
        right="motherboard.memory_type",
        on_fail=["ram"],
        message="📦 ОЗУ несовместима с материнской платой"
    ),
    Rule(
        left="ram.frequency",
        op="<=",
        right="motherboard.memory_freq_max",
        on_fail=["ram"],
        message="📦 Частота ОЗУ выше поддерживаемой"
    ),
    Rule(
        left="cooler.tdp_max",
        op=">=",
        right="cpu.tdp",
        on_fail=["cooler"],
        message="❄️ Охлаждение не справляется с TDP процессора"
    ),

    # 🎮 GPU должна помещаться в корпус
    Rule(
        left="gpu.length",
        op="<=",
        right="case.max_gpu_length",
        on_fail=["gpu"],
        message="🎮 Видеокарта не помещается в корпус"
    ),
    Rule(
        left="psu.power",
        op=">=",
        right="__psu_required__",
        on_fail=["psu"],
        message="🔌 Недостаточная мощность блока питания"
    ),
]

def resolve(path: str, build: dict):
    if path == "__psu_required__":
        return PSUCalculator.required(build)

    data = build
    for key in path.split("."):
        if key not in data:
            return None
        data = data[key]
    return data

def apply_rules(build: dict):
    messages = []

    for rule in RULES:
        left = resolve(rule.left, build)
        right = resolve(rule.right, build)

        if left is None or right is None:
            continue

        if not OPS[rule.op](left, right):
            for comp in rule.on_fail:
                build.pop(comp, None)
            messages.append(rule.message)

    return build, messages

def is_component_compatible(build: dict, component: dict) -> bool:
    test_build = deepcopy(build)
    test_build[component["type"]] = component

    _, messages = apply_rules(test_build)
    return len(messages) == 0