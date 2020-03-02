# set up logging to file - see previous section for more details
from logging import handlers
import logging


class Log:
    def __init__(self, log_path):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_path)
        # filemode='w')
        # # define a Handler which writes INFO messages or higher to the sys.stderr
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)

        # logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        #
        logHandler = handlers.TimedRotatingFileHandler(filename=log_path, when='midnight',
                                                       interval=1,
                                                       encoding='utf-8')
        logHandler.suffix = "%Y%m%d"
        # logHandler.setFormatter(logFormatter)l

        # logger set
        logger = logging.getLogger('myLogger')
        logger.setLevel(logging.INFO)
        logger.addHandler(logHandler)
        logger.addHandler(consoleHandler)
