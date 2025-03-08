'''
A singleton class to handle conversations.
'''

from openai import OpenAI
import discord

import config
from services.Controller import Controller
from services import elevenlabs

class ConversationController(Controller):
    conversation = []
    def __init__(self) -> None:
        super().__init__()
        self.conversation = [{"role": "system", "content": config.system_prompt}]

    def generate_llm_response(self, user_input) -> str:
        client = OpenAI()
        
        # Prepare input for LLM
        message = {"role":"user", "content": user_input}
        self.conversation.append(message)
        
        # Send input to LLM
        print("Sending request to OpenAI")
        print(str(self.conversation))
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.conversation) 
        print("Received response from OpenAI")
        
        # Append the LLM response to the end of the conversation
        self.conversation.append(completion.choices[0].message)
        return self.conversation[-1].content
    
    def generate_voice_file(ctx, raw_response):
        return elevenlabs.elevenlabs_generate(ctx, raw_response)

    def play_voice_file(ctx, response):
        # Process and play received audio
        if response.status_code == 200:
            with open("wav_file.wav", "wb") as local_file:
                local_file.write(response.content)
            audio_source = discord.FFmpegPCMAudio('./wav_file.wav')
            ctx.voice_client.play(audio_source)
        else:
            ctx.respond(f"Voice playback failed. Received status code {response.status_code}")