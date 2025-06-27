from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Column
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog import DialogManager
from aiogram.types import Message, CallbackQuery

from states import TaskDialogSG
from services import fetch_tasks, create_task


# --- MENU ---
async def start_menu(message: Message, dialog_manager: DialogManager):
    token = dialog_manager.start_data.get("token")
    if token:
        dialog_manager.dialog_data["token"] = token
    else:
        await message.answer("❌ Токен не передан.")
    await dialog_manager.switch_to(TaskDialogSG.menu)


menu_window = Window(
    Const("📋 Главное меню"),
    Column(
        SwitchTo(Const("📌 Мои задачи"), id="tasks", state=TaskDialogSG.tasks),
        SwitchTo(Const("➕ Добавить задачу"), id="add", state=TaskDialogSG.add_title),
    ),
    state=TaskDialogSG.menu,
)


# --- VIEW TASKS ---
async def tasks_getter(dialog_manager: DialogManager, **_):
    token = dialog_manager.start_data.get("token") or dialog_manager.dialog_data.get("token")
    if not token:
        return {"tasks": "", "no_tasks": True}

    tasks = await fetch_tasks(token)

    if not isinstance(tasks, list):  # fail-safe
        return {"tasks": "⚠️ Ошибка получения задач", "no_tasks": True}

    formatted_tasks = "\n\n".join(
        f"📌 <b>{t['title']}</b>  (ID: <code>{t['id']}</code>)\n"
        f"📂 Категория: <i>{t['category']}</i>\n"
        f"📝 Описание: {t['description'] or '—'}\n"
        f"📅 Создана: {t['created_date']}\n"
        f"⏰ Дедлайн: {t['due_date']}\n"
        f"✅ Выполнено: {'Да' if t['is_completed'] else 'Нет'}"
        for t in tasks
    )

    return {
        "tasks": formatted_tasks,
        "no_tasks": not tasks
    }


tasks_window = Window(
    Format("📌 Ваши задачи:\n\n{tasks}", when="tasks"),
    Const("❗️ У вас нет задач.", when="no_tasks"),
    Button(Const("⬅ Назад"), id="back", on_click=lambda *a: a[2].switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.tasks,
    getter=tasks_getter
)


# --- ADD TASK TITLE ---
async def title_handler(message: Message, widget, manager: DialogManager, *args):
    manager.dialog_data["title"] = message.text
    await manager.switch_to(TaskDialogSG.add_due_date)

title_window = Window(
    Const("Введите заголовок задачи:"),
    TextInput(id="title_input", on_success=title_handler),
    Button(Const("❌ Отмена"), id="cancel", on_click=lambda *a: a[2].switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.add_title,
)


# --- ADD TASK DATE ---
async def due_date_handler(message: Message, widget, manager: DialogManager, *args):
    manager.dialog_data["due_date"] = message.text
    await manager.switch_to(TaskDialogSG.finish)

due_date_window = Window(
    Const("Введите дату (ISO: 2025-01-01T15:00:00):"),
    TextInput(id="date_input", on_success=due_date_handler),
    Button(Const("❌ Отмена"), id="cancel", on_click=lambda *a: a[2].switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.add_due_date,
)


# --- FINISH TASK CREATION ---
async def finish_handler(callback: CallbackQuery, button, manager: DialogManager):
    data = manager.dialog_data
    token, title, due = data.get("token"), data.get("title"), data.get("due_date")

    success, msg = await create_task(token, title, due)
    await callback.message.answer(msg)
    await manager.switch_to(TaskDialogSG.menu)

finish_window = Window(
    Const("Создать задачу?"),
    Button(Const("✅ Создать"), id="confirm", on_click=finish_handler),
    Button(Const("❌ Назад"), id="cancel", on_click=lambda *a: a[2].switch_to(TaskDialogSG.menu)),
    state=TaskDialogSG.finish,
)

async def on_dialog_start(start_data: dict, dialog_manager: DialogManager):
    token = start_data.get("token")
    if token:
        dialog_manager.dialog_data["token"] = token

dialog = Dialog(menu_window, tasks_window, title_window, due_date_window, finish_window, on_start=on_dialog_start)
