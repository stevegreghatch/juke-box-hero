import logging
import uvicorn
from fastapi import FastAPI
from main.backendService.service.JukeBoxHeroService import process_job
from main.backendService.utility.Sanitize import sanitize_url

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/download_mp3')
async def download_mp3(url: str):
    logger.info('received request to process job')
    url = sanitize_url(url)
    downloaded_file, tempo, key = process_job(url)
    return {'downloaded_file': downloaded_file, 'tempo': tempo, 'key': key}

def main():
    logger.info('Starting FastAPI application')
    uvicorn.run(app, port=8080, host='0.0.0.0', access_log=False)


if __name__ == '__main__':
    main()
