import json
from log import logger as mylogger
from datetime import datetime
from wires import *

if __name__ == '__main__':
    target = 'osen'
    # if target == '' :
    #     print('not found target')
    #     # 에러 종료.
    #     exit(1)
    # logger = log.logger
    mylogger.info('START GET REMOTE FILE TARGET: ' + target)

    # config.json read
    with open('./config/config.json', 'r') as f:
        config = json.load(f)
        env = config[target]

    # 해당 년,월 까지만 스캔 e.g) 2020/01
    today = datetime.now().strftime('%Y/%m/%d')

    hostname = env['server']
    username = env['user']
    password = env['password']
    localDirectoryPath = env['local_file_path'] + '/' + target
    remoteDirectoryPath = env['remote_file_path']

    ssh_session = SSHSession(hostname=hostname, username=username, password=password,
                             local_directory=localDirectoryPath, remote_directory=remoteDirectoryPath)
    # ssh_session.sftp.cwd(remoteDirectoryPath)

    types = ['img', 'xml']
    for type in types:

        target_dir = remoteDirectoryPath + '/' + type + '/' + today
        # print(target_dir)
        if ssh_session.exist_remote_directory(target_dir):
            ssh_session.get_all(ssh_session.filelist_recursive(target_dir).items())

    ssh_session.sftp.close()
