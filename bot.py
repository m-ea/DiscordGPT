import dotenv
import os
import openai
import discord
import requests
import io

# Update the system prompt to provide high-level instructions before the conversation begins.
system_prompt = "You are a helpful AI assistant."

### AUTH ###
dotenv.load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_KEY")
elevenLabs_key = {"xi-api-key": os.getenv("ELEVENLABS_KEY")}

bot = discord.Bot()
stream_endpoint = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM/stream"

### OPENAI ###
conversation = [{"role": "system", "content": system_prompt}]
def convo(input):
    message = {"role":"user", "content": input}
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation) 
    conversation.append(completion.choices[0].message)
    return conversation[-1]["content"]

### DISCORD ###
@bot.slash_command(name="chatgpt", description = "Submit a message to ChatGPT.")
async def chatgpt(ctx, message: discord.Option(str, "The text to send to ChatGPT")):

    global conversation
    
    # Send text to ChatGPT
    await ctx.defer()
    if len(conversation) == 1:
        await ctx.respond("New conversation started. Please wait...")
    raw_response = convo(message)
    response = f"**Input:** {message}\n\n**Response:** {raw_response}"
    await ctx.respond(response)
        
    # Stream audio to voice if connected
    if ctx.author.voice is not None:
        request_body = {"text": raw_response, "voice_settings": {"stability": 0, "similarity_boost": 0}}
        response = requests.post(stream_endpoint, json=request_body, headers=elevenLabs_key)
        if response.status_code == 200:
            print(str(response.status_code))
            audio_file = io.BytesIO(response.content)
            audio_source = discord.FFmpegPCMAudio.read(audio_file)
            ctx.voice_client.play(audio_source)
        else:
            await ctx.respond("Voice playback failed. Did not receive a proper response from ElevenLabs.")

@bot.slash_command(name = "reset", description = "Reset the conversation.")
async def join(ctx):
    global conversation
    conversation = [{"role": "system", "content": system_prompt}]
    await ctx.respond("Conversation ended.")

@bot.slash_command(name = "join", description = "Make the bot join the voice channel to which you are connected.")
async def join(ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        await ctx.respond("You need to be in a voice channel to use this command.")
        return

    voice_channel = voice_state.channel

    await voice_channel.connect()

    try:
        await ctx.guild.change_voice_state(channel=voice_channel)
    except discord.errors.ClientException:
        await ctx.respond("I'm already in a voice channel.")
    except Exception as e:
        await ctx.respond(f"An error occurred: {e}")

    await ctx.respond(f"Connected to {voice_channel}")

@bot.slash_command(name="leave", description = "Make the bot leave voice chat.")
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.respond("Not connected to a voice channel.")
        return

    # Disconnect the bot from the voice channel
    await ctx.voice_client.disconnect()
    await ctx.respond("Disconnected from the voice channel.")

bot.run(os.getenv("TOKEN"))