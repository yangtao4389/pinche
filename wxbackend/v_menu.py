import requests
from django.shortcuts import HttpResponse


class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        postData = postData.encode("utf-8")
        ret =requests.post(url=postUrl,data=postData)
        return ret.content

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        ret = requests.post(url=postUrl)
        return ret.content

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        ret = requests.post(url=postUrl)
        return ret.content

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        ret = requests.post(url=postUrl)
        return ret.content