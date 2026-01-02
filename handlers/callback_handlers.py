from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
import keyboard.inline_keyboard as inkb
callback_router = Router()
from fsm.states import BuildState
@callback_router.callback_query(F.data == "build_pc")
async def build_pc(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(build={})
    await state.set_state(BuildState.menu)

    await callback_query.message.answer(
        "🧩 Конфигуратор ПК\nВыберите компонент:",
        reply_markup=inkb.build_menu_kb({})
    )
async def debug_callback(callback: CallbackQuery):
    print(callback.data)
    await callback.answer()