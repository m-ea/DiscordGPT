import requests
import discord
import json

from services.BotConstruct import bot
import services.elevenlabs as elevenlabs
from services.elevenlabs import elevenLabs_key

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

@bot.slash_command(name="voices", description = "Select the voice to use in voice chat.")
async def voices(ctx):
    voices = get_voices()
    voice_options = []

    for voice in voices:
        voice_options.append(discord.SelectOption(label=voice["name"], description=voice["voice_id"]))

    select = discord.ui.Select(
        placeholder="Choose which voice to use.",
        options = voice_options
    )

    async def callback(interaction):
        print(select.values[0])
        for voice in voices:
            if voice["name"] == select.values[0]:
                elevenlabs.voiceId = voice["voice_id"]
                print("Setting voice ID: " + elevenlabs.voiceId)
                elevenlabs.build_endpoint()
                continue
        await interaction.response.send_message(f"Selected {select.values[0]}")

    select.callback = callback
    view = discord.ui.View()
    view.add_item(select)
    await ctx.respond("Choose which voice to use in voice chat.", view=view)