import dotenv
import os
import openai
import discord
import requests
import json

# Update the system prompt to provide high-level instructions before the conversation begins.
system_prompt = "You are a helpful AI assistant."

### AUTH ###
dotenv.load_dotenv('.env')
openai.api_key = os.getenv("OPENAI_KEY")
try:
    elevenLabs_key = {"xi-api-key": os.getenv("ELEVENLABS_KEY")}
except:
    print("No ElevenLabs API key detected. Voice will not function.")

bot = discord.Bot()

### OPENAI ###
conversation = [{"role": "system", "content": system_prompt}]
def convo(input):
    global conversation
    message = {"role":"user", "content": input}
    conversation.append(message)
    print("Sending request to OpenAI")
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation) 
    print("Received response from OpenAI")
    conversation.append(completion.choices[0].message)
    return conversation[-1]["content"]

### ELEVENLABS ###
def get_voices():
    voices = []
    voice_endpoint = "https://api.elevenlabs.io/v1/voices"
    response = requests.get(voice_endpoint, headers=elevenLabs_key)
    print(f"ElevenLabs get voices response code: {response.status_code}")
    if response.status_code == 200:
        converted_response = json.loads(response.content.decode('utf-8'))
        for i in converted_response["voices"]:
            voices.append(i)
    return voices

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
    stream_endpoint = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    if ctx.author.voice is not None:
        # Create, send, and receive ElevenLabs content
        request_body = {"text": raw_response, "voice_settings": {"stability": 0.25, "similarity_boost": 0.75}}
        response = requests.post(stream_endpoint, json=request_body, headers=elevenLabs_key)
        print(f"ElevenLabs response code: {response.status_code}")
        
        # Process and play received audio
        if response.status_code == 200:
            with open("wav_file.wav", "wb") as local_file:
                local_file.write(response.content)
            audio_source = discord.FFmpegPCMAudio('./wav_file.wav')
            ctx.voice_client.play(audio_source)
        else:
            await ctx.respond(f"Voice playback failed. Received status code {response.status_code}")

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

@bot.slash_command(name="voices", description = "Select the voice to use in voice chat.")
async def voices(ctx):
    voices = get_voices()
    voice_options = []

    for voice in voices:
        voice_options.append(discord.SelectOption(label=voice["name"], description=voice["category"]))

    select = discord.ui.Select(
        placeholder="Choose which voice to use.",
        options = voice_options
    )

    view = discord.ui.View()
    view.add_item(select)
    await ctx.respond("Choose which voice to use in voice chat.", view=view)

bot.run(os.getenv("TOKEN"))