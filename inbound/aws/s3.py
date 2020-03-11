import boto3
import logging


class S3Session(object):
    """
    S3 세션을 위한 클래스 정의.

    """
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, bucket_name):
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      region_name=region_name)

        # self.s3_client = boto3.client('s3')
        self.bucket = bucket_name

        self.logger = logging.getLogger("%s" % self.__class__.__qualname__)

    def file_upload(self, file_obj, file_key):
        """
        S3 파일 업로드 메소드.
        :param file_obj:
        :param file_key:
        :return:
        """
        try:
            self.s3_client.upload_fileobj(file_obj, Bucket=self.bucket, Key=file_key)
            self.logger.info('SUCCESS Upload s3 bucket key: {%s}' % file_key)

        except Exception as e:
            self.logger.error('ERROR Upload s3 bucket key: {%s}, msg: {%s}' % (file_key, e))
