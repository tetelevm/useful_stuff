"""
A script to run a bot with some small logic.
This is useful when you need something from the bot once.
"""

import asyncio
from ast import literal_eval
from pathlib import Path

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler
from telegram.constants import ParseMode
from telegram.ext.filters import ChatType, TEXT


def parse_envs() -> dict:
    try:
        with open(Path(__file__).parent / ".envs", "r") as file:
            text = file.readlines()
    except FileNotFoundError:
        raise ValueError("Requires the settings file `.envs`")

    clean_text = [line[:line.find("#")] for line in text]
    envs_dict = "{" + ",".join(filter(bool, clean_text)) + "}"
    return literal_eval(envs_dict)

envs = parse_envs()


async def echo(update, context):
    print("there!")
    await update.effective_chat.send_message(
        update.message.text,
        parse_mode=ParseMode.MARKDOWN_V2
    )


async def main():
    TOKEN = envs["TOKEN"]
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(MessageHandler(TEXT & ChatType.PRIVATE, echo, False))
    allowed_updates = [Update.MESSAGE, Update.POLL_ANSWER]

    await bot.initialize()
    await bot.updater.start_polling(allowed_updates=allowed_updates)
    await bot.start()
    print(f"Bot has started")
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
