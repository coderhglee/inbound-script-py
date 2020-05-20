import boto3

# S3 Client 생성
# aws_access_key_id=None, aws_secret_access_key=None,
#                  aws_session_token=None, region_name=None,
#                  botocore_session=None, profile_name=None
boto3.Session(aws_access_key_id='',
              aws_secret_access_key='', region_name='ap-northeast-2')
s3 = boto3.client('s3', aws_access_key_id='',
                  aws_secret_access_key='', region_name='ap-northeast-2')

# S3에있는 현재 버킷리스트의 정보를 가져온다.

# print()

bucket = boto3.resource('s3').Bucket('chosun-arc')
response = s3.list_objects(Bucket='chosun-arc', Prefix='osen', MaxKeys=300)

with open('/get/osen/xml/2020/03/05/202003041201774033.xml',
          'rb') as data:
    print(data)
    print(s3.upload_fileobj(data, Bucket='chosun-arc', Key='osen/xml/2020/03/05/202003041201774033.xml'))
# /Users/hakgyun/repository_chosunbiz/inbound-script-py/get/osen/xml/2020/03/05/202003041158779040.xml

# response = s3.Bucket('chosun-arc')


# response에 담겨있는 Buckets의 이름만 가져와 buckets 변수에 배열로 저장.
# buckets = [bucket['Name'] for bucket in response['Buckets']]

# S3 버킷 리스트를 출력.
# print("Bucket List: %s" % buckets)
