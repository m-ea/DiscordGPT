import discord
from pydub import AudioSegment

# TODO: TD5 This file was for testing music overlaid with elevenlabs voice. Functionality should be built into the chatgpt command instead.

from services.BotConstruct import bot, music_controller

@bot.command(name="merge", description = "play merged audio")
async def merge(ctx):

    mood = music_controller.select_mood()
    music_controller.select_music(mood)

# Debug block to be removed as part of TD5
    #sound1 = AudioSegment.from_file("./1.wav", format="wav")
    #sound2 = AudioSegment.from_file("./2.wav", format="wav")
#
    ## sound1 6 dB louder
    #louder = sound1 + 6
#
    ## Overlay sound2 over sound1 after 3000ms
    #overlay = louder.overlay(sound2, position=3000)
#
#
    ## simple export
    #overlay.export("./wav_file.wav", format="wav")
#
    #audio_source = discord.FFmpegPCMAudio("./wav_file.wav")
    #ctx.voice_client.play(audio_source)