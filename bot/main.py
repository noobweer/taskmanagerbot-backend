import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram_dialog import DialogManager, setup_dialogs, StartMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from dialogs import dialog, TaskDialogSG
from services import get_or_create_user
from config import BOT_TOKEN

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(dialog)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, dialog_manager: DialogManager):
    user = await get_or_create_user(message.from_user.id)
    if not user:
        await message.answer("❌ Не удалось авторизоваться.")
        return

    token = user["user"]["token"]

    await dialog_manager.start(
        TaskDialogSG.menu,
        mode=StartMode.RESET_STACK,
        data={"token": token}
    )


async def main():
    setup_dialogs(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
