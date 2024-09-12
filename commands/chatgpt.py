import discord
from openai import OpenAI

from BotConstruct import bot, system_prompt, elevenLabs_key
import services.elevenlabs as elevenlabs

### OPENAI ###
client = OpenAI()
conversation = [{"role": "system", "content": system_prompt}]
def convo(input):
    global conversation
    message = {"role":"user", "content": input}
    conversation.append(message)
    print("Sending request to OpenAI")
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation) 
    print("Received response from OpenAI")
    conversation.append(completion.choices[0].message)
    return conversation[-1].content

### DISCORD ###
@bot.slash_command(name="chatgpt", description = "Submit a message to ChatGPT.")
async def chatgpt(ctx, message: discord.Option(str, "The text to send to ChatGPT")):
    global conversation

    # Send text to ChatGPT
    await ctx.defer()
    if len(conversation) == 1:
        await ctx.respond("New conversation started. Please wait...")
    raw_response = convo(message)
    print("Posting response to text channel...")
    response = f"**Input:** {message}\n\n**Response:** {raw_response}"
    await ctx.respond(response)
    print("Response posted to text channel.")

    ### ELEVENLABS ###
    if ctx.author.voice is not None:
        elevenlabs.elevenlabs_generate(ctx, raw_response)