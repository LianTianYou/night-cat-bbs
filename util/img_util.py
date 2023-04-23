import base64
import io
from PIL import Image
from util import oss_util

def convert_img(data : bytes, size : int) -> bytes:
    img_bytes = io.BytesIO(data)
    img = Image.open(img_bytes)
    img = img.convert('RGB')
    img.thumbnail((size, size))
    with io.BytesIO() as output:
        img.save(output, 'JPEG', quality=80, optimize=True)
        data = output.getvalue()
    return data

def upload_profile(data : bytes, user_id : int) -> str:
    file_name = f'{user_id}.jpg'
    file_path = f'profile/{file_name}'
    data = convert_img(data, 100)
    oss_util.upload_file(file_path, data)
    return file_name

def upload_post_image(data : bytes, post_id : int, order_number : int):
    file_name = f'{post_id}_{order_number}.jpg'
    file_path = f'post_image/{file_name}'
    data = convert_img(data, 100)
    oss_util.upload_file(file_path, data)
    return file_name

def base_to_bytes(code : str):
    if code:
        start_index = code.find(',')
        if start_index != -1:
            code = code[start_index + 1:]
    data = base64.b64decode(code)
    return data

if __name__ == '__main__':
    pass
    # with open("1.png", 'rb') as f:
    #     data = f.read()
    #     data = convert_img(data, 100)
    #     with open("2.jpg", 'wb') as f2:
    #         f2.write(data)
