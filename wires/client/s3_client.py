import logging

import boto3
from botocore.exceptions import ClientError


class S3Client(object):
    """
    S3 세션을 위한 클래스 정의.

    """

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      region_name=region_name)

        # self.s3_client = boto3.client('s3')

        self.logger = logging.getLogger("%s" % self.__class__.__qualname__)

    def file_obj_upload(self, bucket_name, file_obj, file_key):
        """
        S3 파일 업로드 메소드.
        :param bucket_name:
        :param file_obj:
        :param file_key:
        :return:
        """
        try:
            self.s3_client.upload_fileobj(file_obj, Bucket=bucket_name,
                                          Key=file_key)
        except ClientError as e:
            self.logger.error('ERROR Upload s3 bucket key: {%s}, msg: {%s}' % (file_key, e))
        else:
            self.logger.info('SUCCESS Upload s3 bucket key: {%s}' % file_key)

    def file_upload(self, bucket_name, file_path, file_key):

        try:
            self.s3_client.upload_file(file_path, Bucket=bucket_name, Key=file_key)
        except ClientError as e:
            self.logger.error('ERROR Upload s3 bucket key: {%s}, msg: {%s}' % (file_key, e))
        else:
            self.logger.info('SUCCESS Upload s3 bucket key: {%s}' % file_key)
