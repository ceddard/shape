import datetime
import logging

LOG_DUMP_PATH = 'logs/failure.log'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _log_failure(e):
    with open(LOG_DUMP_PATH, 'a') as fLog:
        fLog.write(f'{datetime.datetime.now()} - Failure: %s\n' % (str(e)))
    logger.error(f'Failure: {str(e)}')
