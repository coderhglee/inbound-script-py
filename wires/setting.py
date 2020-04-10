from configparser import ConfigParser, ExtendedInterpolation
import json
import logging
from logging import config
import os


class Setting:
    def __init__(self):

        print('setting main')
        print('process id:', os.getpid())
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
        # print('setting ok')
