import requests
import json
import time
import hashlib
from common import client,checkparam
from django.shortcuts import HttpResponse
from django.core.cache import cache

from logging import getLogger
logger = getLogger("default")

def verifyToken(request):
    token = "HELLOWORLD"
    signature = request.GET.get("signature")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")
    echostr = request.GET.get("echostr")

    if not(signature and  timestamp  and nonce and echostr):

        return HttpResponse("非法请求")
    list = [token, timestamp, nonce]
    list.sort()

    print(list,'list222')
    sha1 = hashlib.sha1()
    map(sha1.update,list)
    hashcode = sha1.hexdigest()
    print(hashcode,'hashcode')
    print(signature,'signature')

    temp = ''.join(list)
    sha1 = hashlib.sha1(temp.encode('utf-8'))

    hashcode = sha1.hexdigest()
    logger.info("自己的hashcode:%s,微信方的signature:%s"%(hashcode,signature))

    if hashcode == signature:

        return HttpResponse(echostr)
    else:
        return HttpResponse("验证失效")






def real_get_access_token():
    '''
    该方法上线后需要被一直调用，保证access_token一直存在
    或者每次手动去调用，如果有，则直接返回
    :param request:
    :return:
    '''
    APPID = "wx7b27955ce810b11f"
    APPSECRET = "d2754228e5db08f3ce1a1011d59e9798"
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID,APPSECRET)
    try:
        access_token = cache.get("access_token")
        if not access_token:
            responseJson = requests.get(url,timeout=3).text
            responseDict = json.loads(responseJson)
            #{"access_token":"ACCESS_TOKEN","expires_in":7200}
            # {"errcode": 40013, "errmsg": "invalid appid"}
            logger.info("getToken-responseDict%s"%responseDict)
            access_token = responseDict.get("access_token")
            expires_in = responseDict.get("expires_in")
            if access_token and expires_in and checkparam.isVaildInt(expires_in):
                cache.set("access_token",access_token,int(expires_in))
                return access_token
            else:
                raise Exception
        else:
            return access_token
    except:
        logger.exception("获取token出错")
        return False


def getToken(request):
    return HttpResponse(real_get_access_token())


if __name__ == '__main__':
    print(real_get_access_token())



# class TokenRelease():
#     def __index__(self):
#         self.__accessToken = ""
#         self.expires_in = None
#
#     def __real_get_access_token(self):
#         APPID = "wxd2ee708e2f14a707"
#         APPSECRET = "7ea2c0df5e192baa3565bb0b6bed4cc7"
#         url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
#         APPID, APPSECRET)
#         try:
#             responseJson = requests.get(url).text
#             responseDict = json.loads(responseJson)
#             # {"access_token":"ACCESS_TOKEN","expires_in":7200}
#             # {"errcode": 40013, "errmsg": "invalid appid"}
#             logger.info("getToken-responseDict%s" % responseDict)
#             access_token = responseDict.get("access_token")
#             expires_in = responseJson.get("expires_in")
#             if access_token and expires_in:
#                 return access_token, expires_in
#             else:
#                 raise Exception
#         except:
#             logger.exception("获取token出错")
#             return False
#
#     def get_access_token(self):
#
#         if self.__leftTime < 10:
#             self.__real_get_access_token()
#         return self.__accessToken


# import urllib
# import time
# import json
# class Basic:
#     def __init__(self):
#         self.__accessToken = ''
#         self.__leftTime = 0
#     def __real_get_access_token(self):
#         appId = "xxxxx"
#         appSecret = "xxxxx"
#         postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
#         urlResp = urllib.urlopen(postUrl)
#         urlResp = json.loads(urlResp.read())
#         self.__accessToken = urlResp['access_token']
#         self.__leftTime = urlResp['expires_in']
#     def get_access_token(self):
#         if self.__leftTime < 10:
#             self.__real_get_access_token()
#         return self.__accessToken
#     def run(self):
#         while(True):
#             if self.__leftTime > 10:
#                 time.sleep(2)
#                 self.__leftTime -= 2
#             else:
#                 self.__real_get_access_token()
