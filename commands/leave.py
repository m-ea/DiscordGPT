from BotConstruct import bot

@bot.slash_command(name="leave", description = "Make the bot leave voice chat.")
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.respond("Not connected to a voice channel.")
        return

    # Disconnect the bot from the voice channel
    await ctx.voice_client.disconnect()
    await ctx.respond("Disconnected from the voice channel.")