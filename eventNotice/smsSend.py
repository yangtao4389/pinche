# -*- coding: utf-8 -*-
from __future__ import print_function

import ssl, hmac, base64, hashlib,json
from datetime import datetime as pydatetime
from eventNotice.models import EventNoticeSmsSendStatistic
try:
    from urllib import urlencode
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
from logging import getLogger
logger = getLogger("default")


def smsSend(mobile,smsCode):
    # 云市场分配的密钥Id
    secretId = "AKIDm8elxog6rbctezVd04Mpe7i30q9jy5wdisom"
    # 云市场分配的密钥Key
    secretKey = "hPB4Ecr99t7FlX11W56evz4KA3ZedddePofTjX2"
    source = "market"

    # 签名
    datetime = pydatetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signStr = "x-date: %s\nx-source: %s" % (datetime, source)
    sign = base64.b64encode(hmac.new(secretKey.encode('utf-8'), signStr.encode('utf-8'), hashlib.sha1).digest())
    auth = 'hmac id="%s", algorithm="hmac-sha1", headers="x-date x-source", signature="%s"' % (secretId, sign.decode('utf-8'))

    # 请求方法
    method = 'GET'
    # 请求头
    headers = {
        'X-Source': source,
        'X-Date': datetime,
        'Authorization': auth,
    }
    # 查询参数
    queryParams = {
        'mobile': mobile,
        'param': "code:%s"%smsCode,
        'tpl_id': 'TP18031513'}
    # body参数（POST方法下存在）
    bodyParams = {
    }
    # url参数拼接
    url = 'http://service-g9x2885n-1255399658.ap-beijing.apigateway.myqcloud.com/release/smsNotify'
    if len(queryParams.keys()) > 0:
        url = url + '?' + urlencode(queryParams)

    request = Request(url, headers=headers)
    request.get_method = lambda: method
    print(request.get_full_url())
    if method in ('POST', 'PUT', 'PATCH'):
        request.data = urlencode(bodyParams).encode('utf-8')
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    statisticObj = EventNoticeSmsSendStatistic()
    statisticObj.phone = mobile
    try:
        response = urlopen(request, timeout=2)
        content = response.read()
        dictContent = json.loads(content.decode("utf-8"))
        logger.info(dictContent)
        if dictContent:
            statisticObj.return_code = dictContent.get("return_code")
            statisticObj.order_id = dictContent.get("order_id")
            statisticObj.save()
            return True
        else:
            raise Exception
    except:
        logger.exception("发送短信验证码失败")
        statisticObj.return_code = "999"
        statisticObj.save()
        return False
if __name__ == '__main__':
    a = smsSend("18649715651", "1234")
    print(a)