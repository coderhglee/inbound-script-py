from datetime import datetime
import configparser
import logging
import sys
import os
from inbound import *


def main(target):
    """


    """
    # env setting
    env = configparser.ConfigParser()
    try:
        env.read(os.path.abspath('env.ini'))
    except Exception as e:
        print('not found env msg %s' % e)

    env_obj = env['DEFAULT']
    aws_obj = env['AWS']

    # Logger Setting
    Log(logging_config=os.path.abspath(env_obj['LOG_CONFIG_PATH']))
    # Properties Setting
    prop = PropertiesGenerator(config_path=os.path.abspath(env_obj['CONFIG_PATH']), target=target)

    logger = logging.getLogger(__name__)
    logger.info('start get file to : %s' % target)
    logger.info('host: %s user: %s' % (prop.hostname, prop.username))

    try:

        try:
            session = SftpSession(hostname=prop.hostname, username=prop.username, password=prop.password,
                                  local_directory=prop.local_directory_path,
                                  remote_directory=prop.remote_directory_path,
                                  remote_backup_directory=prop.remote_backup_path)
        except Exception as e:
            logger.error('Sftp Session을 연결하는데 문제가 발생했습니다. MSG: %s' % e)

        try:
            s3_session = S3Session(aws_access_key_id=aws_obj['AWS_ACCESS_KEY_ID'],
                                   aws_secret_access_key=aws_obj['AWS_SECRET_ACCESS_KEY'],
                                   region_name=aws_obj['REGION_NAME'],
                                   bucket_name=aws_obj['BUCKET_NAME'])
            # s3_session = S3Session()
        except Exception as e:
            logger.error('S3 Session을 연결하는데 문제가 발생했습니다. MSG: %s' % e)

        # 해당 년,월,일 까지만 스캔 e.g) 2020/01
        today = datetime.now().strftime('%Y/%m/%d')

        for children in prop.remote_child_path:

            target_dir = '%s/%s/%s' % (prop.remote_directory_path, children, today)

            logger.info('target 폴더: %s' % target_dir)
            if session.exist_remote_directory(target_dir):
                # 타겟 폴더로 위치 변경.
                session.sftp.cwd(target_dir)
                # 현제 sftp session의 file list 가져오기.
                file_items = session.file_list_recursive().items()

                for folder, files in file_items:
                    root_path = folder.replace(prop.remote_directory_path, '')

                    for file in files:
                        remote_file = '%s/%s' % (folder, file)
                        bucket_key = "%s%s/%s" % (target, root_path, file)

                        # s3_session.file_upload(file_obj=session.get_file_obj(remote_file_path=remote_file),
                        #                        file_key=bucket_key)

                        with session.sftp.open(remote_file, 'rb') as fl:
                            s3_session.file_upload(file_obj=fl, file_key=bucket_key)

                # session.get_all(file_items)

    except Exception as e:
        logger.error('문제가 발생했습니다. MSG: %s' % e)

    finally:
        session.sftp.close()


if __name__ == '__main__':
    # print('ttttttt'+sys.argv[0])
    main(target=sys.argv[1])
