# from .properties import PropertiesGenerator
# from inbound.logs import LoggerGenerator
import json
from .logs import Log
from .properties import PropertiesGenerator


class ApplicationConfiguration:
    def __init__(self, env, target):
        Log(log_path=env['ROOT_PATH'] + env['LOG_PATH'])
        self.properties = PropertiesGenerator(config_path=env['ROOT_PATH'] + env['CONFIG_PATH'], target=target)
        # with open(root_path + config_path, 'r') as f:
        #     config = json.load(f)
        #     self.env = config[target]
        #     self.hostname = self.env['server']
        #     self.username = self.env['user']
        #     self.password = self.env['password']
        #     self.local_directory_path = self.env['local_file_path']
        #     self.remote_directory_path = self.env['remote_file_path']
        #     self.remote_backup_path = self.env['remote_backup_path']
