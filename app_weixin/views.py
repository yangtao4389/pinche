from django.shortcuts import render, HttpResponse
from py_modules.werobot import WeRoBot
myrobot = WeRoBot(token='HELLOWORLD')


@myrobot.handler
def hello(message):
    return 'Hello World!'