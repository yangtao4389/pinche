from logging import getLogger
logger = getLogger("default")
from py_modules.werobot import WeRoBot

TOKEN = 'HELLOWORLD'
APP_ID = "wx7b27955ce810b11f"
APP_SECRET = "d2754228e5db08f3ce1a1011d59e9798"
myrobot = WeRoBot(token=TOKEN)
myrobot.config["APP_ID"] = APP_ID
myrobot.config["APP_SECRET"] = APP_SECRET



myrobotclient = myrobot.client


from py_modules.werobot.login.login import WeixinLogin
wx_login = WeixinLogin(APP_ID,APP_SECRET)