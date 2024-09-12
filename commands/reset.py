from BotConstruct import bot, system_prompt

@bot.slash_command(name = "reset", description = "Reset the conversation.")
async def reset(ctx):
    global conversation
    conversation = [{"role": "system", "content": system_prompt}]
    await ctx.respond("Conversation ended.")