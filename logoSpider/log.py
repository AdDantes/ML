import logging

logging.basicConfig(level=logging.INFO,
                 format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s: %(message)s ',
                 datefmt='(%Y-%b-%d %H:%M:%S)',
                 filename='./log.log')

logger = logging.getLogger(__name__)

logger.info('dfadas')

