import logging
import os
import requests
import librosa
from librosa.feature import chroma_cqt
import numpy as np
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def process_job(url):
    downloaded_file = download_track(url)
    tempo, key = get_metadata(downloaded_file)
    return downloaded_file, tempo, key


def download_track(url):
    response = requests.get(url)
    filename = os.path.basename(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename


def get_metadata(filename):
    logger.info(f'Loading file: {filename}')
    start_time = time.time()
    try:
        y, sr = librosa.load(filename)
        tempo = int(librosa.beat.beat_track(y=y, sr=sr)[0])
        key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][np.argmax(np.sum(chroma_cqt(y=y, sr=sr), axis=1))]
        logger.info(f'File loaded successfully in {time.time() - start_time:.2f} seconds')
        return tempo, key
    except Exception as e:
        logger.error(f'Error loading file: {e}')
        raise
