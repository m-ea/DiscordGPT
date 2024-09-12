import os

from BotConstruct import bot

from commands import join, leave, merge, reset, voices, chatgpt

bot.run(os.getenv("TOKEN"))