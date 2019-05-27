import os
from logging import getLogger
logger = getLogger("default")
from django.conf import settings
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

from py_modules.werobot.mp.mp import WeixinMP
jt_path = os.path.join(settings.BASE_DIR, ".weixin_jsapi_ticket")
ac_path = os.path.join(settings.BASE_DIR, ".weixin_access_token")

wx_map = WeixinMP(APP_ID,APP_SECRET,ac_path=ac_path, jt_path=jt_path)
# 通过该wx_map 可以直接获取 全局微信  access_token  jsapi_ticket  nonce_str  还有其他关于微信平台的方法

template_id_001 = "" # ***
template_id_002 = "" # ***
template_id_003 = "" # ***
