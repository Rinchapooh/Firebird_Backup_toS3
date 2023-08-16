import datetime
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config

load_dotenv()

user = os.environ.get('user')
password = os.environ.get('password')
archive_pass = os.environ.get('archive_pass')
path_to_base = os.environ.get('path_to_base')
path_to_backup = os.environ.get('path_to_backup')
base_file = os.environ.get('base_file')
curedate = f"{datetime.datetime.now():%d_%m_%Y_}"
backup_file = curedate + os.environ.get('backup_file')
final_name = backup_file + '.7zip'
full_bak_path = path_to_backup + backup_file
gz_filename = full_bak_path + '.gz'


endpoint_url = os.environ.get('endpoint_url')
region_name = os.environ.get('region_name')
bucket_name = os.environ.get('bucket_name')
account_name = os.environ.get('account_name')
secret_key = os.environ.get('secret_key')

BUCKET = {'Name': bucket_name}




# BackUp Firebird base with a gbak utility and zip file
os.system(f'gbak -B -G '
          f' -user {user}'
          f' -password {password}'
          f' {path_to_base}{base_file}'
          # f' {path_to_backup}{backup_file} -v && gzip -v {full_bak_path}')
          f' {path_to_backup}{backup_file} -v && 7za a -sdel -p{archive_pass} {final_name} {full_bak_path} ')

# Create S3Boto client
s3client = boto3.client(
    's3',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=account_name,
    aws_secret_access_key=secret_key,
    config=Config(s3={'addressing_style': 'path'})
)

# Upload to the S3 storage
with open(final_name, 'rb') as data:
    s3client.upload_fileobj(data, BUCKET['Name'], final_name)
