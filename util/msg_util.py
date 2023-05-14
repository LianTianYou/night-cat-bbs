from tables import LastAccess

def get_msg():
    last_access = LastAccess.query.all()
    access_list = []
    for i in last_access:
        access = dict()
        access['msg_type'] = i.msg_type
        access['last_id'] = i.last_id
        access_list.append(access)
    return access_list