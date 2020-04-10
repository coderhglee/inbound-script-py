import logging
from multiprocessing import Process

from wires.job import LocalJob, SftpJob
from wires.setting import Setting
from wires.process import JobProcess

if __name__ == '__main__':

    # Global Setting
    setting = Setting()

    logger = logging.getLogger(__name__)

    procs = []

    for target_config in setting.target_config_json:

        # name = target_config['name']
        # active = target_config['active']
        # protocol = target_config['protocol']
        #
        # if active:
        #
        #     if protocol == 'local':
        #         job = LocalJob(env=setting.env, config=target_config, name=name)
        #
        #     elif protocol == 'sftp':
        #         job = SftpJob(env=setting.env, config=target_config, name=name)
        #
        #     logger.info("Start Job {target: %s, protocol: %s}" % (name, protocol))
        #
        #     # job.run()
        job_process = JobProcess(env=setting.env, config=target_config)
        proc = Process(target=job_process.execute_job)
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()
