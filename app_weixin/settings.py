from logging import getLogger
logger = getLogger("default")
from py_modules.werobot import WeRoBot

myrobot = WeRoBot(token='HELLOWORLD')
myrobot.config["APP_ID"] = "wx7b27955ce810b11f"
myrobot.config["APP_SECRET"] = "d2754228e5db08f3ce1a1011d59e9798"



myrobotclient = myrobot.client