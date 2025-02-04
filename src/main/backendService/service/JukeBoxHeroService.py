import librosa
import requests


def download_mp3(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_metadata():
    y, sr = librosa.load("track.mp3")
    bpm, _ = librosa.beat.beat_track(y=y, sr=sr)
    # key = librosa.key.key(y)
    