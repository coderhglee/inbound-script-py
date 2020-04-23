import json
from logging import config as logConfig


class Log:
    def __init__(self, config_path, file_path):
        with open(config_path, 'rt') as f:
            log_config_json = json.load(f)
            # log_file_name = self.config['name'] + '_wires.logs'
            log_config_json['handlers']['file_handler']['filename'] = file_path
            logConfig.dictConfig(log_config_json)
            # logging.config.dictConfig(log_config_json)
