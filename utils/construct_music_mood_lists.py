import config
import json

# music library operations explained:
# EXAMPLE: library.get("music")[1].get("id")
#
# library is the dict where all music schema lives
# music is the root object
# [1] is the index in the music list, which corresponds to the track id
# id is the dict key defined in the schema

def construct_music_mood_lists():
    music_list_rousing = []
    music_list_cheerful = []
    music_list_brooding = []
    music_list_silly = []
    music_list_intense = []
    with open(config.MUSIC_LIBRARY_FILE) as file:
        library = json.load(file)
        for track in library.get("music"):
            # Gets a list of moods for the track being iterated on
            track_moods = track.get("tags")[0].get("moods")
            
            if "rousing" in track_moods:
                music_list_rousing.append(track.get("id"))
            elif "cheerful" in track_moods:
                music_list_cheerful.append(track.get("id"))
            elif "brooding" in track_moods:
                music_list_brooding.append(track.get("id"))
            elif "silly" in track_moods:
                music_list_silly.append(track.get("id"))
            elif "intense" in track_moods:
                music_list_intense.append(track.get("id"))

    return music_list_rousing, music_list_cheerful, music_list_brooding, music_list_silly, music_list_intense