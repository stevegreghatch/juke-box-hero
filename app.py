import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from main.backendService.service.JukeBoxHeroService import process_job

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/process_audio')
async def process_audio(artist: str, track_name: str):
    logger.info('received request to process job')
    file_path, pre_signed_url, bpm, key = process_job(artist, track_name)
    logger.info('job processed successfully')
    return {'file_path': file_path,'pre_signed_url': pre_signed_url,
            'bpm': bpm, 'key': key}

def main():
    logger.info('Starting FastAPI application')
    uvicorn.run(app, port=8080, host='0.0.0.0', access_log=False)


if __name__ == '__main__':
    main()
