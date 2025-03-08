import requests
import dotenv
import os

import config

### AUTH ###
print("Loading Elevenlabs API key")
dotenv.load_dotenv('.env')
try:
    elevenLabs_key = {"xi-api-key": os.getenv("ELEVENLABS_KEY")}
except:
    print("No ElevenLabs API key detected. Voice will not function.")
    config.voice_output_enabled = False

### END AUTH ###

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
    return response