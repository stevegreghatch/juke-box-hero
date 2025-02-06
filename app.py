import logging
import uvicorn
from fastapi import FastAPI
from main.backendService.service.JukeBoxHeroService import process_job

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/process_audio')
async def process_audio(artist: str, track_name: str):
    logger.info('received request to process job')
    downloaded_file, tempo, key = process_job(artist, track_name)
    logger.info(f'job processed successfully -- downloaded_file: {downloaded_file}, tempo: {tempo}, key: {key}')
    return {'downloaded_file': downloaded_file, 'tempo': tempo, 'key': key}

def main():
    logger.info('Starting FastAPI application')
    uvicorn.run(app, port=8080, host='0.0.0.0', access_log=False)


if __name__ == '__main__':
    main()
