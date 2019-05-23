from django.shortcuts import render, HttpResponse
from py_modules.werobot import WeRoBot
from .settings import myrobot,logger




@myrobot.handler
def hello(message):
    return 'Hello World!'

# @myrobot.key_click("music")
# def music(message):
#     return '你点击了“今日歌曲”按钮'

@myrobot.click
def abort(message):
    if message.key == "key1":  #我要拼车
        return "该项目趋于功能完善阶段，目前差一台服务器跟域名，有赞助的朋友嘛？微信(18649715651)"
    elif message.key == "key2":
        return "http://211.149.180.119/admin/login"