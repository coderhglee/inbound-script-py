import logging
import os
from multiprocessing import Process

from wires.process import JobProcess
from wires.setting import Setting

if __name__ == '__main__':

    # Global Setting
    setting = Setting()

    logger = logging.getLogger(__name__)

    logger.info('********************************* WIRES AGENT IS START ***********************************')

    working_target = os.environ['WORKING_TARGET']

    procs = []
    for target_config in setting.target_config_json:
        active = target_config['active']

        if active:
            job_process = JobProcess(env=setting.env, config=target_config)
            proc_obj = Process(target=job_process.execute_job)
            proc_obj.start()
            logger.info("Start Job {pid: %s, target: %s, protocol: %s}" % (
                proc_obj.pid, target_config['name'], target_config['protocol']))
            # print(proc_obj.pid)
            procs.append(proc_obj)

    for proc in procs:
        proc.join()
