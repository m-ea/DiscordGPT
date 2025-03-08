from services.BotConstruct import bot
import config

@bot.slash_command(name = "reset", description = "Reset the conversation.")
async def reset(ctx):
    global conversation
    conversation = [{"role": "system", "content": config.system_prompt}]
    await ctx.respond("Conversation ended.")