import discord
import dotenv
import os
import logging

### AUTH ###
dotenv.load_dotenv('.env')
try:
    elevenLabs_key = {"xi-api-key": os.getenv("ELEVENLABS_KEY")}
except:
    print("No ElevenLabs API key detected. Voice will not function.")

logging.basicConfig(level=logging.INFO)

# Update the system prompt to provide high-level instructions before the conversation begins.
system_prompt = "You are a helpful AI assistant."

bot = discord.Bot()