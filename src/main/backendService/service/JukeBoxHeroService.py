import logging
import librosa
from librosa.feature import chroma_cqt
import numpy as np
import time
import internetarchive as ia
import os
import boto3
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def process_job(artist, track_name):
    search_query = f'{artist} {track_name}'
    downloaded_file = get_audio(search_query)
    if not downloaded_file:
        logger.info("Download URL not found.")
        return None
    tempo, key = get_metadata(downloaded_file)
    return downloaded_file, tempo, key

def get_audio(search_query):
    search_results = ia.search_items(f'title:({search_query}) AND mediatype:(audio)')
    for result in search_results:
        files = ia.get_files(result['identifier'])
        for file in files:
            if file.format in ['VBR MP3', 'MP3', 'FLAC', 'OGG']:
                filename = file.name
                item = ia.get_item(result['identifier'])
                download_dir = 'downloads'
                os.makedirs(download_dir, exist_ok=True)
                item.download(files=[filename], destdir=download_dir)
                parent_dir = os.path.join(download_dir, result['identifier'])
                full_path = os.path.join(parent_dir, filename)
                s3_key = f'{os.getenv('S3_PREFIX')}{filename}'
                boto3.client('s3').upload_file(full_path, os.getenv('S3_BUCKET_NAME'), s3_key)
                logger.info(f'File uploaded to S3: {s3_key}')
                return full_path
    return None

def get_metadata(file_path):
    logger.info('Processing audio data')
    start_time = time.time()
    try:
        y, sr = librosa.load(file_path, sr=None)
        tempo = int(librosa.beat.beat_track(y=y, sr=sr)[0])
        key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][np.argmax(np.sum(chroma_cqt(y=y, sr=sr), axis=1))]
        os.remove(file_path)
        logger.info(f'Audio data processed successfully in {time.time() - start_time:.2f} seconds')
        return tempo, key
    except Exception as e:
        logger.error(f'Error processing audio data: {e}')
        raise