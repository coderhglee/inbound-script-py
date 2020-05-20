import json
import os
from configparser import ConfigParser, ExtendedInterpolation

from wires.log import Log


class Setting:
    def __init__(self):

        # print('setting main')
        # print('process id:', os.getpid())
        """
        Global Setting init
        """
        ENV_PATH = os.environ['ENV_PATH']
        self.env = ConfigParser(interpolation=ExtendedInterpolation())

        try:
            self.env.read(ENV_PATH)
        except Exception as e:
            print('not found env msg %s' % e)

        # self.env = env['DEFAULT']
        # print(os.environ['WORK_PATH'])
        # print(self.default_env['LOG_CONFIG_PATH'])

        with open(self.env['DEFAULT']['CONFIG_PATH'], 'rt') as f:
            self.target_config_json = json.load(f)

        Log(config_path=self.env['DEFAULT']['LOG_CONFIG_PATH'],
            file_path="%s%s" % (self.env['DEFAULT']['LOG_PATH'], 'wires.logs'))
