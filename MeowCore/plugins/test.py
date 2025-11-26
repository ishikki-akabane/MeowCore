### Test Plugin - XYGHA

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


@Client.on_message(filters.command("test"))
async def test_command(client, message):
    name = message.from_user.first_name
    await message.reply_text(f"Hello {name}!! This is a Test")


