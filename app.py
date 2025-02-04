import logging
import uvicorn
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/programs')
async def get_programs():
    logger.info('received request to get all programs')
    return 'sample_response'


def main():
    logger.info('Logger configured')
    logger.info('Starting FastAPI application')
    uvicorn.run(app, port=8080, host='0.0.0.0', access_log=False)


if __name__ == '__main__':
    main()
