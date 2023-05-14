import uuid
import requests
import hashlib
import time

from util.config_util import get_value

URL = 'http://openapi.youdao.com/api'
APP_KEY = get_value('oss', 'key')
APP_SECRET = get_value('oss', 'secret')

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(URL, data=data, headers=headers)

def query(q):
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)

    data = {
        'curtime': curtime,
        'from': 'auto',
        'to': 'auto',
        'signType': 'v3',
        'appKey': APP_KEY,
        'q': q,
        'salt': salt,
        'sign': sign,
        'vocabId': "2C1E6A6AD119482BB0CD2381F3359521",
        'ext':'wav',
        'voice':'0',

    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    html = requests.post(URL, data=data, headers=headers)
    return html.json()

if __name__ == '__main__':
    result = query("box")