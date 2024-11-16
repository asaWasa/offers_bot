from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

offers_keyboard = IKM(
    inline_keyboard=[
        [
            IKB(text="❌", callback_data="del_post"),
            IKB(text="🤬", callback_data="ban_user"),
            IKB(text="🧹", callback_data="clear_user_post"),
            IKB(text="⏳", callback_data="send_deferred_post"),
            IKB(text="✅", callback_data="send_post"),
        ]
    ]
)
