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
    DB_REDIS_URL,
    DB_REDIS_PORT,
    SLEEP_FOR_FORWARD_TASK_SEC,
)
from modules.keyboards.admin_inlines import offers_keyboard
from modules.redis.orders import Redis
import signal


redis = Redis(url=DB_REDIS_URL, port=DB_REDIS_PORT)
bot = Bot(token=API_KEY, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Событие для остановки фоновой таски
stop_event = asyncio.Event()


def new_user(func):
    async def wrapper(msg: types.Message):
        user_id = msg.from_user.id

        return await func(msg, False)

    return wrapper


@dp.message(Cmd("start"))
@new_user
async def cmd_start(
    msg: types.Message,
    is_new_user: bool = False,
):
    if is_new_user:
        chat = await bot.get_chat(MAIN_CHANNEL_ID)
        await msg.answer(f"Привет! это бот с предложкой для канала {chat.invite_link}")
    await msg.answer(f"Чтобы предложить пост, просто пришли картинку с подписью.")


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

        # chat = await bot.get_chat(ADMIN_CHANNEL_ID)
        # logger.info(f"ID : {msg.from_user.id}")
        # await bot.send_photo(
        #     chat.id,
        #     photo=msg.photo[-1].file_id,
        #     caption=f"Новое сообщение в предложке от {msg.from_user.full_name}(@{msg.from_user.username})!\n"
        #     f"Описание: {msg.caption if msg.caption is not None else 'Пусто ('}",
        #     reply_markup=offers_keyboard,
        # )


async def shutdown(dispatcher: Dispatcher):
    stop_event.set()


async def main() -> None:
    await dp.start_polling(bot)


async def forward_to_channel(stop_event):
    while not stop_event.is_set():
        image_data = await redis.lpop("image_queue")
        if image_data:
            chat_id, file_id, caption = image_data.decode().split("|")
            await bot.send_photo(MAIN_CHANNEL_ID, file_id, caption=caption)

        await asyncio.sleep(SLEEP_FOR_FORWARD_TASK_SEC)


if __name__ == "__main__":
    logger = logging.getLogger()
    if LOGGING:
        logging.basicConfig(
            level=logging.INFO,
        )
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(forward_to_channel(stop_event))
        for signal_type in [signal.SIGINT, signal.SIGTERM]:
            loop.add_signal_handler(
                signal_type, lambda: asyncio.ensure_future(shutdown(dp))
            )
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logger.info("Exit")
    except Exception as e:
        logger.error(f"ERROR : {e}")
