import logging

from wires.job import LocalJob, SftpJob
from wires.log import Log


class JobProcess:
    def __init__(self, env, config):
        self.env = env
        self.config = config
        self.logger = logging.getLogger("%s_%s" % (self.config['name'], self.__class__.__qualname__))
        """
        로그 설정 및 파일경로 json import
        """
        Log(config_path=env['DEFAULT']['LOG_CONFIG_PATH'],
            file_path="%s%s_%s" % (self.env['DEFAULT']['LOG_PATH'], self.config['name'], 'wires.logs'))
        # with open(env['DEFAULT']['LOG_CONFIG_PATH'], 'rt') as f:
        #     log_config_json = json.load(f)
        #     log_file_name = self.config['name'] + '_wires.logs'
        #     log_config_json['handlers']['file_handler']['filename'] = self.env['DEFAULT']['LOG_PATH'] + log_file_name
        #
        #     logging.config.dictConfig(log_config_json)

    def execute_job(self):

        name = self.config['name']
        protocol = self.config['protocol']

        if protocol == 'local':
            job = LocalJob(env=self.env, config=self.config, name=name)

        elif protocol == 'sftp':
            job = SftpJob(env=self.env, config=self.config, name=name)

        self.logger.info("Start Job {target: %s, protocol: %s}" % (name, protocol))

        job.run()
