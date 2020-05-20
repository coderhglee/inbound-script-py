import json
import logging
from logging import config


class Log:
    def __init__(self, logging_config):
        """
        로그 설정 및 파일경로 json import
        :param logging_config:
        """
        with open(logging_config, 'rt') as f:
            config_json = json.load(f)

        logging.config.dictConfig(config_json)

        # logger = logging.getLogger()
        # 루트 로거 설정.
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                     datefmt='%Y-%m-%d %H:%M:%S',
        #                     filename=log_path)
        # logging.config.dictConfig()
        # # filemode='w')
        # # # define a Handler which writes INFO messages or higher to the sys.stderr
        # logConsoleHandler = logging.StreamHandler()
        # logConsoleHandler.setLevel(logging.INFO)
        #
        # # logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        # #
        #
        # logFileHandler = handlers.TimedRotatingFileHandler(filename=log_path, when='midnight',
        #                                                    interval=1,
        #                                                    encoding='utf-8')
        # logFileHandler.suffix = "%Y%m%d"
        # # logHandler.setFormatter(logFormatter)
        # # logger set
        # rootLogger = logging.getLogger()
        # rootLogger.setLevel(logging.INFO)
        # rootLogger.addHandler(logFileHandler)
        # rootLogger.addHandler(logConsoleHandler)
