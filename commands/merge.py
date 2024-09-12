import discord
from pydub import AudioSegment

from BotConstruct import bot

@bot.command(name="merge", description = "play merged audio")
async def merge(ctx):
    sound1 = AudioSegment.from_file("./1.wav", format="wav")
    sound2 = AudioSegment.from_file("./2.wav", format="wav")

    # sound1 6 dB louder
    louder = sound1 + 6

    # Overlay sound2 over sound1 at position 0  (use louder instead of sound1 to use the louder version)
    overlay = louder.overlay(sound2, position=0)


    # simple export
    overlay.export("./wav_file.wav", format="wav")

    audio_source = discord.FFmpegPCMAudio("./wav_file.wav")
    ctx.voice_client.play(audio_source)