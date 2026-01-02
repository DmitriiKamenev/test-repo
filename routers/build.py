from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from fsm.states import BuildState
from services.json_loader import load_components, get_by_id
from services.rule_engine import apply_rules
from services.pricing import total_price
from keyboard.inline_keyboard import build_menu_kb, components_kb,card_kb
from services.configurator import get_available_components
from services.card import build_card

router = Router()

@router.callback_query(F.data.startswith("change:"))
async def change_component(call: CallbackQuery, state: FSMContext):
    component = call.data.split(":")[1]

    data = await state.get_data()
    build = data.get("build", {})

    available = get_available_components(component, build)

    await state.update_data(choosing=component)
    await state.set_state(BuildState.choosing)

    await call.message.edit_text(
        f"Выберите {component}:",
        reply_markup=components_kb(available)
    )

@router.callback_query(BuildState.choosing, F.data.startswith("select:"))
async def select_component(call: CallbackQuery, state: FSMContext):
    _, ctype, cid = call.data.split(":")

    data = await state.get_data()
    build = data.get("build", {})

    build[ctype] = get_by_id(ctype, cid)
    build, messages = apply_rules(build)

    await state.update_data(build=build)
    await state.set_state(BuildState.menu)

    if messages:
        await call.message.answer("⚠️\n" + "\n".join(messages))

    await call.message.edit_text(
        "✅ Компонент выбран",
        reply_markup=build_menu_kb(build)
    )

@router.callback_query(F.data == "summary:price")
async def show_price(call: CallbackQuery, state: FSMContext):
    build = (await state.get_data()).get("build", {})
    price = total_price(build)

    await call.message.edit_text(
        f"💰 Итоговая стоимость: *{price} ₽*",
        parse_mode="Markdown",
        reply_markup=build_menu_kb(build)
    )

@router.callback_query(F.data == "summary:card")
async def show_card(call: CallbackQuery, state: FSMContext):
    build = (await state.get_data()).get("build", {})
    if not build:
        await call.message.edit_text("❌ Сборка пуста")
        return

    await call.message.edit_text(
        build_card(build),
        parse_mode="Markdown",
        reply_markup=card_kb()
    )

@router.callback_query(F.data == "card:back")
async def card_back(call: CallbackQuery, state: FSMContext):
    """Вернуться в конфигуратор"""
    build = (await state.get_data()).get("build", {})
    await call.message.edit_text(
        "🧩 Вернулись в конфигуратор. Выберите компонент:",
        reply_markup=build_menu_kb(build)
    )

@router.callback_query(F.data == "card:checkout")
async def card_checkout(call: CallbackQuery, state: FSMContext):
    """Дальнейшее оформление"""
    build = (await state.get_data()).get("build", {})
    price = total_price(build)
    await call.message.edit_text(
        f"📝 Оформление сборки\nИтоговая стоимость: {price} ₽\n\n"
        "📌 На этом шаге можно добавить интеграцию с платёжной системой "
        "или отправку сборки на email/telegram."
    )