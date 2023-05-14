def set_ok(data : dict, msg : str = None):
    set_data(data, msg, 'ok')

def set_no(data : dict, msg : str = None):
    set_data(data, msg, 'no')

def load_data(msg : str = None) -> dict:
    data = {
        'data': dict(),
        'status': 'no'
    }
    if msg:
        data['data']['msg'] = msg
    return data
def set_data(data : dict, msg : str, status : str = None):
    if msg:
        data['data']['msg'] = msg
    data['status'] = status