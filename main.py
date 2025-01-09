# in & as LazyDeveloper
# Please Don't Remove Credit

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
import asyncio


# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


# Start Command Handler
@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
    try:
        await event.reply_photo(
            "https://telegra.ph/file/2b160d9765fe080c704d2.png",
            caption=Config.START_MSG.format(event.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔺 Donate us 🔺", url="https://p.paytm.me/xCTH/vo37hii9")],
                [InlineKeyboardButton("⚡️ LazyDeveloper ⚡️", url="https://t.me/LazyDeveloper")],
                [
                    InlineKeyboardButton("🤒Help", callback_data="Help_msg"),
                    InlineKeyboardButton("🦋About", callback_data="About_msg")
                ]
            ])
        )
    except Exception as e:
        print(f"[Start Handler Error] - {e}")


# Help Command Handler
@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(_, event: Message):
    try:
        await event.reply_text(
            Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Updates", url="https://t.me/LazyDeveloper"),
                    InlineKeyboardButton("Support Group", url="https://t.me/LazyPrincessSupport"),
                    InlineKeyboardButton("About", callback_data="About_msg")
                ]
            ])
        )
    except Exception as e:
        print(f"[Help Handler Error] - {e}")


# Inline Search Handler
@Bot.on_message(filters.incoming)
async def inline_handlers(_, event: Message):
    if event.text == "/start":
        return

    answers = (
        f"**📂 Hunts For ➠ {event.text} \n"
        f"⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟤\n"
        f"🔊\n"
        f"➠ Type Only Movie Name With Correct Spelling. Don't type Bhejo, Bhej Do, send me etc...✍️\n"
        f"➠ Add Year For Better Result.🗓️\n"
        f"⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟥⟤\n\n**"
    )

    async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.text):
        if message.text:
            f_text = message.text.split("|||", 1)[0] if "|||" in message.text else message.text
            lines = f_text.split("\n")
            title = lines[0] if len(lines) > 0 else "No Title Found"
            url = lines[-1] if len(lines) > 1 else "No URL Found"
            answers += (
                f"**🎞 Movie Title ➠ {title}\n\n"
                f"📜 Download URLs ➠ {url}\n\n"
                f"▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
                f"Link Will Auto Delete In 35Sec...⏰\n"
                f"▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**"
            )

    try:
        msg = await event.reply_text(answers)
        await asyncio.sleep(35)
        await event.delete()
        await msg.delete()
    except Exception as e:
        print(f"[Inline Handler Error] - {e}")


# Callback Query Handler
@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
    cb_data = cmd.data

    try:
        if "About_msg" in cb_data:
            await cmd.message.edit(
                text=Config.ABOUT_BOT_TEXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Updates Channel", url="https://t.me/LazyDeveloper")],
                    [
                        InlineKeyboardButton("Connect Admin", url="https://t.me/LazyDeveloper"),
                        InlineKeyboardButton("🏠Home", callback_data="gohome")
                    ]
                ]),
                parse_mode="html"
            )
        elif "Help_msg" in cb_data:
            await cmd.message.edit(
                text=Config.ABOUT_HELP_TEXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("Help", callback_data="Help_msg"),
                        InlineKeyboardButton("Updates Channel", url="https://t.me/LazyDeveloper")
                    ],
                    [
                        InlineKeyboardButton("Connect Admin", url="https://t.me/LazyDeveloper"),
                        InlineKeyboardButton("🏠Home", callback_data="gohome")
                    ]
                ]),
                parse_mode="html"
            )
        elif "gohome" in cb_data:
            await cmd.message.edit(
                text=Config.START_MSG.format(cmd.from_user.mention),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("Help", callback_data="Help_msg"),
                        InlineKeyboardButton("About", callback_data="About_msg")
                    ],
                    [InlineKeyboardButton("Support Channel", url="https://t.me/LazyPrincessSupport")]
                ]),
                parse_mode="html"
            )
    except QueryIdInvalid:
        await cmd.answer("Invalid Query ID!", show_alert=True)
    except Exception as e:
        print(f"[Callback Query Error] - {e}")


# Start Clients
Bot.start()
User.start()

# Loop Clients till Disconnects
idle()

# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
