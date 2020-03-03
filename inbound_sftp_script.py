from datetime import datetime
# from inbound.config import ApplicationConfiguration
# import config
# from inbound.config import *
# from inbound.sftp import *
import configparser
import logging
import sys
from inbound import config
from inbound import sftp


def main(target):
    env = configparser.ConfigParser()
    env.read('env.ini')

    # print(config['DEFAULT']['WorkingPath'])
    # env = configparser.ConfigParser().read('env.ini')
    env_obj = env['DEFAULT']
    # Logger Setting
    config.Log(log_path=env_obj['ROOT_PATH'] + env_obj['LOG_PATH'])
    # Properties Setting
    prop = config.PropertiesGenerator(config_path=env_obj['ROOT_PATH'] + env_obj['CONFIG_PATH'], target=target)

    logger = logging.getLogger('myLogger')
    logger.info('start get file to : ' + target)
    logger.info('host: ' + prop.hostname + ' user: ' + prop.username)

    try:
        session = sftp.SftpSession(hostname=prop.hostname, username=prop.username, password=prop.password,
                                   local_directory=prop.local_directory_path,
                                   remote_directory=prop.remote_directory_path,
                                   remote_backup_directory=prop.remote_backup_path)

        children_dir = ['img', 'xml']

        # 해당 년,월,일 까지만 스캔 e.g) 2020/01
        today = datetime.now().strftime('%Y/%m/%d')

        for children in children_dir:

            target_dir = prop.remote_directory_path + '/' + children + '/' + today

            logger.info('target 폴더: ' + target_dir)
            if session.exist_remote_directory(target_dir):
                # 타겟 폴더로 위치 변경.
                session.sftp.cwd(target_dir)
                # 현제 sftp session의 file list 가져오기.
                file_items = session.file_list_recursive().items()
                # logger.info("new file size: " + len(file_items))

                # 새로운 파일들을 모두 가져옴.
                session.get_all(file_items)

    except Exception as e:
        logger.error(e)

    finally:
        session.sftp.close()


if __name__ == '__main__':
    # print('ttttttt'+sys.argv[1])
    main(target=sys.argv[1])
