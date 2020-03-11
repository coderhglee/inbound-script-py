import json


class PropertiesGenerator:
    def __init__(self, config_path, target):
        # config.json read

        with open(config_path, 'r') as f:
            config = json.load(f)
            self.env = config[target]
            self.hostname = self.env['server']
            self.username = self.env['user']
            self.password = self.env['password']
            self.local_directory_path = self.env['local_file_path']
            self.remote_directory_path = self.env['remote_file_path']
            self.remote_child_path = self.env['remote_child_path']
            self.remote_backup_path = self.env['remote_backup_path']
