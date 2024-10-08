# DiscordGPT
 Discord bot that delivers text to ChatGPT, then outputs it to a Discord text channel. Optionally, it can connect to voice and read the response via ElevenLabs voice generation.

## Installation
- Set up a Discord bot by following the Discord documentation. Only do the Overview and Creating An App sections. https://discord.com/developers/docs/getting-started
- Create a file called .env in the DiscordGPT folder. It needs to contain your credentials:
```
TOKEN=paste your discord app token
OPENAI_API_KEY=paste your OpenAI API key
ELEVENLABS_KEY=paste your ElevenLabs API key
```
- Create a Python virtual environment in the DiscordGPT folder and install dependencies. Execute these commands when DiscordGPT is the current working directory:
```pip install pipenv```
```pipenv shell```
```pipenv update```
- Optional - If using voice, install ffmpeg and include it in your PATH environment variable. Voice will not work without it.
    https://ffmpeg.org/download.html
- Optional - Change the system_prompt variable in BotConstruct.py. This allows you to provide high-level instructions before conversations begin.
- Run the bot:
```python bot.py```

## Usage
### Text commands
- "/chatgpt message:your_text_here" in any text channel the bot can see will send the text to ChatGPT.
- "/reset" will end the current conversation.

### Voice commands
- "/join" will make the bot join the voice channel to which you are connected.
- "/leave" will make the bot leave voice chat.
- "/voices" will display a selection menu that will allows to select which voice from your ElevenLabs account to use.
- If the bot is connected to voice chat, it will read the response generated by "/chatgpt".

Conversations persist across text channels. This means if you say something in one channel, the bot will remember it in any other channel until "/reset" is used.

## Known issues
- There is no error handling. When an error occurs, it will not appear in Discord. The bot will appear to be stuck "thinking". It will still respond to subsequent commands.
- Responses from ChatGPT longer than 2000 characters trigger an exception.
    - If this happens, you can still get the response by asking the AI to repeat the first 2000 characters of the previous response, then the next 2000 characters, and so forth until the response is exhausted.
- If you get rate limited by the OpenAI API, an exception is triggered.
- Some requests to the OpenAI API hang and don't ever time out. I will add a timeout function eventually.
- Requires Python 3.10, does not work with Python 3.11. I have not investigated this yet.
- When multiple requests are made concurrently while the bot is connected to voice, an exception is triggered and the audio skips to the most recently generated audio file.
- There is an arbitrary timeout on the voice selection menu (/voices). If the interaction fails, just call /voices again.

## Future plans
- Add error handling.
- Add config
- Add music feature that can dynamically select Udio tracks from your Udio profile and play them under the Elevenlabs VO