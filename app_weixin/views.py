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
    if message.key == "key1":
        return "我要拼车"
    elif message.key == "key2":
        return "http://211.149.180.119/admin/login"