import requests
import discord

from BotConstruct import elevenLabs_key

# Default voice ID. This changes at runtime if /voices is executed
voiceId = "EXAVITQu4vr4xnSDxMaL"

# Builds the Elevenlabs endpoint
def build_endpoint():
    global stream_endpoint
    stream_endpoint = ("https://api.elevenlabs.io/v1/text-to-speech/" + voiceId)

def elevenlabs_generate(ctx, raw_response):
    build_endpoint()
    print("Endpoint built with voice ID: " + voiceId)
    # Create, send, and receive ElevenLabs content
    request_body = {"text": raw_response, "voice_settings": {"stability": 0.25, "similarity_boost": 0.75}}
    response = requests.post(stream_endpoint, json=request_body, headers=elevenLabs_key)
    print(f"ElevenLabs response code: {response.status_code}")
    
    # Process and play received audio
    if response.status_code == 200:
        with open("wav_file.wav", "wb") as local_file:
            local_file.write(response.content)
        audio_source = discord.FFmpegPCMAudio('./wav_file.wav')
        ctx.voice_client.play(audio_source)
    else:
        ctx.respond(f"Voice playback failed. Received status code {response.status_code}")