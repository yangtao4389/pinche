'''
主要是短连接生成
'''
import requests
import json


def get_short_url(long_url):
    '''
    成功则返回短链接，没成功则啥都不返回
    :param long_url:
    :return:
    '''
    host = 'https://dwz.cn'
    path = '/admin/v2/create'
    url = host + path
    method = 'POST'
    content_type = 'application/json'

    # TODO: 设置Token
    token = '28d648fc22d57a8b22190a068acb21ba'

    # TODO：设置待创建的长网址
    bodys = {'url': long_url}

    # 配置headers
    headers = {'Content-Type': content_type, 'Token': token}

    # 发起请求
    response = requests.post(url=url, data=json.dumps(bodys), headers=headers)

    # 读取响应
    if response.status_code=="200":
        data = json.loads(response.content)
        if data.get('Code') == 0:
            return data.get("ShortUrl")





if __name__ == '__main__':
    base_url = "https://www.baidu.com/"

    short_url = get_short_url(base_url)
    print(short_url)
    # http://dwz.cn/oHvt1KD7

    # long_url = get_long_url(short_url)
    # print(long_url)
    # https://www.baidu.com/
