import time,hashlib,re
def isVaildDate(date):
    '''
    判断日期格式是否符合标准
    :param self:
    :param date:
    :return:
    '''
    try:

        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False
def isVaildDateTime(datetime):
    '''
    判断日期格式是否符合标准
    :param self:
    :param date:
    :return:
    '''
    try:
        time.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False

def isVaildInt(data):
    try:
        int(data)
        return True
    except:
        return False


def get_md5(string):
    hash_md5 = hashlib.md5(string.encode("utf-8"))
    md5_string = hash_md5.hexdigest()
    return md5_string

def checkTelPhone(phone):
    phone_pat = re.compile(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = phone_pat.match(phone)
    if res:
        return True
    else:
        return False

if __name__ == '__main__':
    print(checkTelPhone("18649a5651"))
