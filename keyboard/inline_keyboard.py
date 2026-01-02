from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

startKeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Собрать мой ПК", callback_data="build_pc")],
            [
                InlineKeyboardButton(text="Отзывы", callback_data="reviews")]
            ]
    )

LABELS = {
    "cpu": "🧠 CPU",
    "motherboard": "🧩 MB",
    "ram": "📦 RAM",
    "gpu": "🎮 GPU",
    "cooler": "❄️ Охлаждение",
    "psu": "🔌 БП>",
    "case": "🖥 Корпус"
}

def build_menu_kb(build: dict):
    kb = []
    for key, label in LABELS.items():
        name = build.get(key, {}).get("name", "—")
        kb.append([
            InlineKeyboardButton(
                text=f"{label}: {name}",
                callback_data=f"change:{key}"
            )
        ])

    kb.append([
        InlineKeyboardButton(
            text="💰 Стоимость",
            callback_data="summary:price"
        ),
        InlineKeyboardButton(
            text="📝 Карточка сборки",
            callback_data="summary:card"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb)

def components_kb(components: list[dict]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{c['name']} — {c['price']} ₽",
                    callback_data=f"select:{c['type']}:{c['id']}"
                )
            ]
            for c in components
        ]
    )

def card_kb():
    """Кнопки в карточке сборки: назад и оформить"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="card:back"
                ),
                InlineKeyboardButton(
                    text="✅ Оформить",
                    callback_data="card:checkout"
                )
            ]
        ]
    )