from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command as Cmd
from aiogram.enums import ParseMode
import asyncio
from aiogram.client.default import DefaultBotProperties
import logging
from config import (
    API_KEY,
    LOGGING,
    ADMIN_CHANNEL_ID,
    MAIN_CHANNEL_ID,
)
from keyboards.admin_inlines import offers_keyboard

bot = Bot(token=API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(Cmd("start"))
async def cmd_start(msg: types.Message):
    chat = await bot.get_chat(MAIN_CHANNEL_ID)
    await msg.answer(f"Привет! это бот с предложкой для канала {chat.invite_link}")


@dp.message(Cmd("get_channel_id"))
async def cmd_get_channel_id(msg: types.Message):
    await msg.answer(f"chat id : {msg.chat.id}")


@dp.message(F.photo)
async def handle_photo(msg: types.Message):
    if msg.chat.id == int(ADMIN_CHANNEL_ID):
        await msg.reply(
            text=f"Пост от админа @{msg.from_user.username}",
            reply_markup=offers_keyboard,
        )
    else:
        await msg.reply("Отлично! фото отправлено админам")
        chat = await bot.get_chat(ADMIN_CHANNEL_ID)
        logger.info(f"ID : {msg.from_user.id}")
        await bot.send_photo(
            chat.id,
            photo=msg.photo[-1].file_id,
            caption=f"Новое сообщение в предложке от {msg.from_user.full_name}(@{msg.from_user.username})!\n"
            f"Описание: {msg.caption if msg.caption is not None else 'Пусто ('}",
            reply_markup=offers_keyboard,
        )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger = logging.getLogger()
    if LOGGING:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logger.info("Exit")
    except Exception as e:
        logger.error(f"ERROR : {e}")
