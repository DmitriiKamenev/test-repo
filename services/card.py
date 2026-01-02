from services.pricing import total_price
from services.psu_calculator import PSUCalculator

def build_card(build: dict) -> str:
    lines = ["🖥 *Финальная сборка ПК*:", ""]

    # Компоненты + факты
    for key in ["cpu","motherboard","ram","gpu","cooler","psu","case"]:
        comp = build.get(key)
        if not comp:
            lines.append(f"❌ {key.upper()}: не выбрано")
        else:
            fact = comp.get("fact", "")
            lines.append(f"✅ {comp['name']} — *{comp.get('price',0)} ₽* {fact}")

    # Итоговая стоимость
    price = total_price(build)
    lines.append(f"\n💰 *Итоговая стоимость:* {price} ₽")

    # Потребление системы
    cpu_tdp = build.get("cpu", {}).get("tdp",0)
    gpu_tdp = build.get("gpu", {}).get("tdp",0)
    system_tdp = cpu_tdp + gpu_tdp + 70
    lines.append(f"⚡ Потребление системы: {system_tdp} W (с запасом ~30%)")

    # Блок питания
    psu = build.get("psu")
    if psu:
        coverage = round((system_tdp / psu["power"]) * 100)
        lines.append(f"🔌 Блок питания: {psu['power']}W, потребление {coverage}%")

    # USB порты корпуса
    case = build.get("case")
    if case:
        usb_ports = case.get("usb_ports", 0)
        lines.append(f"🖱 Корпус: {usb_ports} USB портов спереди")

    return "\n".join(lines)
