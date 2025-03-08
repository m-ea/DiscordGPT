import discord

import config
from services.BotConstruct import bot

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

    config.voice_output_enabled = True

    await ctx.respond(f"Connected to {voice_channel}")