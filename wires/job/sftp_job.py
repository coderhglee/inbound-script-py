import logging
import re
import time
from stat import S_ISREG

import schedule

from wires.client import SftpClient, S3Client


class SftpJob:

    def __init__(self, env, config, name):
        self.msg = "I'm working..."
        self.env = env
        self.logger = logging.getLogger("%s_%s" % (name, self.__class__.__qualname__))

        self.sftp_obj = config
        self.aws_obj = self.env['AWS']

        self.s3_client = S3Client(aws_access_key_id=self.aws_obj['AWS_ACCESS_KEY_ID'],
                                  aws_secret_access_key=self.aws_obj['AWS_SECRET_ACCESS_KEY'],
                                  region_name=self.aws_obj['REGION_NAME'])

        self.bucket_name = "%s-%s" % (self.sftp_obj['name'], self.aws_obj['BUCKET_NAME'])
        # TODO: 스케쥴 시간 config 추가
        schedule.every(self.sftp_obj['polling']).seconds.do(self.handler)
        # schedule.every().hour.do(self.handler)
        # schedule.every().day.at("10:30").do(job)
        # schedule.every(5).to(10).minutes.do(job)
        # schedule.every().monday.do(job)
        # schedule.every().wednesday.at("13:15").do(job)
        # schedule.every().minute.at(":17").do(job)

    def handler(self):
        try:
            sftp_client = SftpClient(hostname=self.sftp_obj['server'], username=self.sftp_obj['user'],
                                     password=self.sftp_obj['password'],
                                     remote_directory=self.sftp_obj['remote_file_path'])

            stats = sftp_client.sftp.listdir_attr('.')

            for attr in stats:

                # bool(re.match("^(.(.*\\.jpg$|.*\\.jpeg|.*\\.png))*$", "       test.jpg")
                if S_ISREG(attr.st_mode) & bool(re.match(self.sftp_obj['file_patterns'], attr.filename)):
                    sftp_target_file_path = sftp_client.sftp.getcwd() + '/' + attr.filename
                    with sftp_client.sftp.open(sftp_target_file_path, 'rb') as fl:

                        key = "%s/%s" % (self.sftp_obj['s3_key'], attr.filename)
                        # file_key = 'photo/' + attr.filename

                        self.s3_client.file_obj_upload(bucket_name=self.bucket_name, file_obj=fl,
                                                       file_key=key)

                        sftp_client.del_file(sftp_target_file_path)

        except Exception as e:
            self.logger.error('문제가 발생했습니다. MSG: %s' % e)
        finally:
            sftp_client.sftp.close()

    def run(self):
        try:
            # print('process id:', os.getpid())
            while True:
                schedule.run_pending()
                time.sleep(5)

        except Exception as e:
            self.logger.info(e)
            self.logger.info("Job Stop!!")
