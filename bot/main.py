from aiogram import Bot, Dispatcher
from aiogram.client.session import aiohttp
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types
from aiogram.filters import Command

from aiogram_dialog import DialogManager, Window, Dialog, setup_dialogs, StartMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Column, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.common import ManagedWidget

import aiohttp

from states import TaskDialogSG
from services import get_or_create_user, fetch_tasks
from config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# === Меню ===
async def start(message: types.Message, dialog_manager: DialogManager):
    token = dialog_manager.start_data.get("token")
    if token:
        dialog_manager.dialog_data["token"] = token
    else:
        await message.answer("⚠️ Токен не был передан")
    await dialog_manager.switch_to(TaskDialogSG.menu)


menu_window = Window(
    Const("📋 Главное меню"),
    Column(
        SwitchTo(Const("📋 Мои задачи"), id="tasks", state=TaskDialogSG.tasks),
        SwitchTo(Const("➕ Добавить задачу"), id="add_task", state=TaskDialogSG.add_title),
    ),
    state=TaskDialogSG.menu,
)


# === Просмотр задач ===
async def tasks_getter(dialog_manager: DialogManager, **kwargs):
    token = dialog_manager.dialog_data.get("token")
    tasks = await fetch_tasks(token)

    formatted_tasks = "\n".join(
        f"• {task['title']} ({task['due_date']})" for task in tasks
    ) if tasks else ""

    return {
        "tasks": formatted_tasks,
        "no_tasks": not tasks,
    }


tasks_window = Window(
    Format("Ваши задачи:\n\n{tasks}\n\nДля добавления новой задачи нажмите ➕", when="tasks"),
    Const("У вас нет задач.", when="no_tasks"),
    Button(Const("⬅ Назад"), id="back", on_click=lambda c, b, d: d.switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.tasks,
    getter=tasks_getter,
)


# === Добавление задачи: заголовок ===
async def title_handler(message: types.Message, widget: ManagedTextInput, manager: DialogManager):
    manager.dialog_data["title"] = message.text
    await manager.next()


title_window = Window(
    Const("Введите заголовок задачи:"),
    TextInput(id="title_input", on_success=title_handler),
    Button(Const("❌ Отмена"), id="cancel", on_click=lambda c, b, d: d.switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.add_title,
)


# === Добавление задачи: дата ===
async def due_date_handler(message: types.Message, widget: ManagedTextInput, manager: DialogManager):
    manager.dialog_data["due_date"] = message.text
    await manager.next()


due_date_window = Window(
    Const("Введите дату выполнения в формате ISO 8601 (например: 2025-04-10T12:00:00):"),
    TextInput(id="due_date_input", on_success=due_date_handler),
    Button(Const("❌ Отмена"), id="cancel", on_click=lambda c, b, d: d.switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.add_due_date,
)


# === Завершение добавления задачи ===
async def finish_adding(callback, button, manager: DialogManager):
    token = manager.dialog_data.get("token")
    title = manager.dialog_data.get("title")
    due_date = manager.dialog_data.get("due_date")

    if not all([token, title, due_date]):
        await callback.message.answer("❌ Не хватает данных для создания задачи.")
        await manager.back()
        return

    data_to_send = {
        "title": title,
        "due_date": due_date,
        "is_completed": False,
        "category": "default",
    }

    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
        try:
            async with session.post("http://backend:8000/api/tasks/", json=data_to_send, headers=headers) as response:
                if response.status == 201:
                    await callback.message.answer("✅ Задача успешно создана!")
                else:
                    error_text = await response.text()
                    await callback.message.answer(f"❌ Ошибка создания задачи: {error_text}")
        except Exception as e:
            await callback.message.answer(f"⚠️ Ошибка подключения к серверу: {e}")

    await manager.back()


finish_window = Window(
    Const("✅ Задача успешно создана!"),
    Button(Const("⬅ Назад"), id="done", on_click=finish_adding),
    state=TaskDialogSG.finish_adding,
)


# === Создание диалога ===
task_dialog = Dialog(
    menu_window,
    tasks_window,
    title_window,
    due_date_window,
    finish_window,
)

dp.include_router(task_dialog)


# === Обработчики команд ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    telegram_id = message.from_user.id
    user_data = await get_or_create_user(telegram_id)

    if not user_data:
        await message.answer("❌ Не удалось авторизоваться.")
        return

    token = user_data["user"]["token"]

    await dialog_manager.start(
        TaskDialogSG.menu,
        mode=StartMode.RESET_STACK,
        data={"token": token}
    )


# === Настройка aiogram-dialog ===
setup_dialogs(dp)


# === Запуск бота ===
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())