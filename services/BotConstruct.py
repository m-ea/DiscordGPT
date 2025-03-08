import discord
import logging

from services.ConversationController import ConversationController
from services.MusicController import MusicController

logging.basicConfig(level=logging.INFO)

print("Creating conversation controller")
conversation_controller = ConversationController()
print("Creating music controller")
music_controller = MusicController()
bot = discord.Bot()