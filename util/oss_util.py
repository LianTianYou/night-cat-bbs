import oss2
from util.config_util import get_value

# 配置参数
access_key_id = get_value('oss', 'key')
access_key_secret = get_value('oss', 'secret')
endpoint = get_value('oss', 'endpoint')
bucket_name = get_value('oss', 'bucket_name')

def get_bucket():
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return bucket

def remove_sep(file_path : str) -> str:
    return file_path.lstrip('/')

def upload_file(file_path : str, data : bytes) -> str:
    bucket = get_bucket()

    file_path = remove_sep(file_path)
    bucket.put_object(file_path, data)
    return f'{get_host()}/{file_path}'

def get_host():
    return f'https://{bucket_name}.{endpoint}'

def delete_file(file_path):
    bucket = get_bucket()

    file_path = remove_sep(file_path)
    bucket.delete_object(file_path)

if __name__ == '__main__':
    delete_file('profile/QQ.jpg')