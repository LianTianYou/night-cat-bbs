import oss2

# 配置参数
access_key_id = 'LTAI5tLXBajfzGbUBifqKAiH'
access_key_secret = '9R6k3JUZ71Z3DJrXu1wUGTFR0NwHoz'
endpoint = 'oss-cn-chengdu.aliyuncs.com'
bucket_name = 'night-cat-bbs'

def upload_file(file_path : str, data : bytes) -> str:
    # 创建存储空间实例
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    file_path = file_path.strip('/')
    bucket.put_object(file_path, data)
    return f'{get_host()}/{file_path}'

def get_host():
    return f'https://{bucket_name}.{endpoint}'
