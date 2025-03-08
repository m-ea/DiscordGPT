'''
A singleton class to handle playback and selection of music.
'''

from services.Controller import Controller
from utils.construct_music_mood_lists import construct_music_mood_lists

# Used for debug
import random

class MusicController(Controller):
    def __init__(self) -> None:
        super().__init__()
        currentGenre = ''
        currentMood = ''
        music_list_rousing, music_list_cheerful, music_list_brooding, music_list_silly, music_list_intense = construct_music_mood_lists() # Each list consists of the ids of all the tracks in that genre
    # Will need methods like new track, manual genre/mood specification, etc

    # DEBUG
    def get_random_mood(self):
        moods = ['rousing', 'cheerful', 'brooding', 'silly', 'intense']
        return random.choice(moods)

    def select_mood(self):
        # TODO: Replace get random mood with a music selection method
        mood = self.get_random_mood()
        self.currentMood = mood
        print('Current mood set to: ' + self.currentMood)

    # Uses a genre and a mood to select a track from the library
    # TODO: TD3 Write the method
    def select_music(self, moodSelection):
        pass