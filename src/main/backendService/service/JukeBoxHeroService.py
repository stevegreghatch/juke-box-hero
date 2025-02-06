import logging
import os
import requests
import librosa
from librosa.feature import chroma_cqt
import numpy as np
import time
from werkzeug.utils import secure_filename

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

SAFE_DIRECTORY = '/safe/directory'

def process_job(url):
    downloaded_file = download_track(url)
    tempo, key = get_metadata(downloaded_file)
    return downloaded_file, tempo, key


def download_track(url):
    response = requests.get(url)
    filename = secure_filename(os.path.basename(url))
    fullpath = os.path.normpath(os.path.join(SAFE_DIRECTORY, filename))
    if not fullpath.startswith(SAFE_DIRECTORY):
        raise Exception("Invalid file path")
    with open(fullpath, 'wb') as file:
        file.write(response.content)
    return fullpath


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
