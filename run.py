import logging
from app import create_app

# Setup logger for the runner
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logger = logging.getLogger('MAIN')

app = create_app('config.Config')


if __name__ == "__main__":
    logger.info('=================== IQVIA FLASK SERVER STARTED ===================')
    app.run(host='0.0.0.0', port=5000, debug=True)