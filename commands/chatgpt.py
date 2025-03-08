import discord
from openai import OpenAI

import config
from services.BotConstruct import bot, conversation_controller
import services.elevenlabs as elevenlabs
from services.ConversationController import ConversationController

### DISCORD ###
@bot.slash_command(name="chatgpt", description = "Submit a message to ChatGPT.")
async def chatgpt(ctx, message: discord.Option(str, "The text to send to ChatGPT")):
    await ctx.defer()
    
    # Alert user if starting a new conversation
    print(str(len(ConversationController.conversation) == 1))
    if len(ConversationController.conversation) == 1 and config.text_output_enabled:
        await ctx.respond("New conversation started. Please wait...")
    
    # Generate the response
    raw_response = ConversationController.generate_llm_response(conversation_controller, message)

    if config.text_output_enabled:

        # TODO: TD2 If a response is longer than 2000 characters, it must be broken into several Discord messages. Include the input in the first one, then each subsequent message should contain under 2000 characters until the reply is exhausted.
        # This fix can be implemented in a util

        # Format the response for Discord text channel
        response = f"**Input:** {message}\n\n**Response:** {raw_response}"

        # Send response to Discord
        print("Posting response to text channel...")
        await ctx.respond(response)
        print("Response posted to text channel.")

    ### ELEVENLABS ###
    if config.voice_output_enabled:
        response = ConversationController.generate_voice_file(ctx, raw_response)
        ConversationController.play_voice_file(ctx, response)