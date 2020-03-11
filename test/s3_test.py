import unittest
import boto3
import os


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, False)
        print(os.path.abspath('log'))

    def test_s3(self):
        # S3 Client 생성
        # aws_access_key_id=None, aws_secret_access_key=None,
        #                  aws_session_token=None, region_name=None,
        #                  botocore_session=None, profile_name=None
        boto3.Session(aws_access_key_id='',
                      aws_secret_access_key='', region_name='ap-northeast-2')
        s3 = boto3.client('s3', aws_access_key_id='',
                          aws_secret_access_key='',
                          region_name='ap-northeast-2')

        # S3에있는 현재 버킷리스트의 정보를 가져온다.

        print(boto3.resource('s3').Bucket('chosun-arc'))

        response = s3.list_objects(Bucket='chosun-arc', Prefix='osen', MaxKeys=300)

        print(response)
        print('list all in the bucket')

        # response = s3.Bucket('chosun-arc')

        # response에 담겨있는 Buckets의 이름만 가져와 buckets 변수에 배열로 저장.
        # buckets = [bucket['Name'] for bucket in response['Buckets']]

        # S3 버킷 리스트를 출력.
        # print("Bucket List: %s" % buckets)

if __name__ == '__main__':
    unittest.main()
