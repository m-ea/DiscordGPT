import interactions
import dotenv
import os
import openai

# Update the system prompt to provide high-level instructions before the conversation begins.
system_prompt = "You are a helpful AI assistant."

### AUTH ###
dotenv.load_dotenv('.env')
bot = interactions.Client(token=os.getenv("TOKEN"))
openai.api_key = os.getenv("OPENAI_KEY")

### OPENAI ###
conversation = [{"role": "system", "content": system_prompt}]
def convo(input):
    message = {"role":"user", "content": input}
    conversation.append(message)
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=conversation) 
    conversation.append(completion.choices[0].message)
    return conversation[-1]["content"]

### DISCORD ###
@bot.command()
@interactions.option()
async def chatgpt(ctx: interactions.CommandContext, text: str):
    """Submit a message to ChatGPT or enter reset to start a new conversation."""
    global conversation
    if len(conversation) == 1:
        await ctx.send("Conversation started. Enter \"/chatgpt reset\" to start a new conversation. Please wait...")
    if text != "reset":
        await ctx.defer()
        response = f"**Input:** {text}\n\n**Response:** {convo(text)}"
        await ctx.send(response)
    else:
        conversation = [{"role": "system", "content": system_prompt}]
        await ctx.send("Conversation ended.")

bot.start()