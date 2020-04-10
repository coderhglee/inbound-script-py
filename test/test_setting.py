import json
from unittest import TestCase


class TestSetting(TestCase):
    def test_json_logging(self):
        with open('/Users/hakgyun/repository_chosunbiz/inbound-script-py/config/logging.json', 'rt') as f:
            config_json = json.load(f)
            config_json['handlers']['file_handler']['filename'] = 'test.log'
            # print(config_json)
        with open('/Users/hakgyun/repository_chosunbiz/inbound-script-py/config/config.json', 'rt') as f:
            target_config_json = json.load(f)
            # print(target_config_json)

            for target in target_config_json:

                if target['active']:

                    protocol = target['protocol']

                    if protocol == 'local':
                        print(target['name'])
                    elif protocol == 'sftp':
                        print(target['name'])
