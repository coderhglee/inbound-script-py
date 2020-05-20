import os
import re
import unittest
from stat import *
from unittest import TestCase

from wires.client import SftpClient, S3Client


class TestSftpJob(TestCase):

    def test_handler(self):
        try:
            sftp_client = SftpClient(hostname='172.31.12.47', username='',
                                     password='',
                                     remote_directory='/webstore/ns-home/newspaper/CMS_repository/data/sports/bak')

            s3 = S3Client(aws_access_key_id='',
                          aws_secret_access_key='+3XDAo',
                          region_name='ap-northeast-2')

            # file_items = sftp_client.file_list_recursive().items()
            stats = sftp_client.sftp.listdir_attr('.')
            # attr.filename for attr in stats if S_ISREG(attr.st_mode)
            for attr in stats:
                print(sftp_client.sftp.getcwd())
                print(attr.filename)
                print(attr.st_mode)
                print(S_ISREG(attr.st_mode))
                if S_ISREG(attr.st_mode):
                    sftp_client.sftp.get(
                        localpath='/Users/hakgyun/repository_chosunbiz/inbound-script-py/temp/' + attr.filename,
                        remotepath=sftp_client.sftp.getcwd() + '/' + attr.filename)

                    with sftp_client.sftp.open(sftp_client.sftp.getcwd() + '/' + attr.filename, 'rb') as fl:
                        print(fl)
                        s3.s3_client.upload_fileobj(fl, Bucket='newsis-inbound-sandbox-chosun',
                                                    Key='photo/' + attr.filename)

        except Exception as e:
            self.logger.error('문제가 발생했습니다. MSG: %s' % e)
        finally:
            sftp_client.sftp.close()

    def test_s3(self):
        s3 = S3Client(aws_access_key_id='',
                      aws_secret_access_key='+3XDAo',
                      region_name='ap-northeast-2',
                      bucket_name='newsis-inbound-sandbox-chosun')

        response = s3.s3_client.list_objects(Bucket='newsis-inbound-sandbox-chosun', MaxKeys=300)

        print(response)

    def test_os(self):
        # s3 = S3Client(aws_access_key_id='',
        #               aws_secret_access_key='',
        #               region_name='ap-northeast-2',
        #               bucket_name='newsis-inbound-sandbox-chosun')
        #
        # s3.s3_client.upload_file(
        #     '/Users/hakgyun/repository_chosunbiz/inbound-script-py/temp/202003100100074530004568.xml',
        #     Bucket='newsis-inbound-sandbox-chosun',
        #     Key='photo/test2.xml')

        print(os.path.basename('/Users/hakgyun/repository_chosunbiz/inbound-script-py/get/tt.logs'))

        # with open('/Users/hakgyun/repository_chosunbiz/inbound-script-py/temp/202003100100074530004568.xml',
        #           'wb') as fl:
        #     print(fl.read())

    def test_file_pattern(self):
        print(bool(re.match("^(.(.*\\.jpg$|.*\\.jpeg|.*\\.png))*$", "       test.jpg")))


if __name__ == '__main__':
    unittest.main()
