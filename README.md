# DiscordGPT
 Discord bot that takes a slash command, delivers text to ChatGPT, then outputs it to a Discord text channel

## Installation
1. Set up a Discord bot by following the Discord documentation. Only do the Overview and Creating An App sections. https://discord.com/developers/docs/getting-started
2. Create a file called .env in the DiscordGPT folder. It needs to contain your credentials:
```
TOKEN=paste your discord app token
OPENAI_KEY=paste your OpenAI API key
```
3. Create a Python virtual environment in the DiscordGPT folder and install dependencies. Execute these commands when DiscordGPT is the CWD:
```pip install pipenv```
```pipenv shell```
```pipenv update```
4. Optional - Change the system_prompt variable in bot.py. This allows you to provide high-level instructions before conversations begin.
5. Run the bot:
```python bot.py```

## Usage
In any text channel, enter "/chatgpt text:your prompt here".

Start a new conversation with "/chatgpt text:reset".

Conversations persist across text channels.

## Known issues
- There is no error handling. When an error occurs, it will not appear in Discord. The bot will appear to be stuck "thinking". It will still respond to subsequent commands.
- Responses from ChatGPT longer than 2000 characters trigger an exception.
    - If this happens, you can still get the response by asking the AI to repeat the first 2000 characters of the previous response, then the next 2000 characters, and so forth until the response is exhausted.
- If you get rate limited by the OpenAI API, an exception is triggered.

## Future plans
- Add error handling.
- Add voice integration with ElevenLabs.