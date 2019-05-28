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

## 车主模板
template_id_001 = "6vNq3GK_vT-sR93q78_yK6dz2iSo_7rpOpCo-Ql8-9w" # ***行程发布成功通知
template_id_002 = "xaRmgH-d59eMl721Ldwk3SiZT5Eu0m6JnQHuDzBa3HI" # 拼车订座通知
template_id_003 = "n-u2NgJ0kSWhuA8TQKQ_mREDPM95w6IsVuiaqTECHXc" # 拼车退订通知

# 乘客模板
template_id_101 = "2DJdM9YN0F4dGnScsWSqX96zzYVcES_mWmISE0vY6SI" #  订座成功通知
template_id_102 = "IBsT2h0MHKRxlKanFWeeuORDFzf2WguuHbBivENZGPo" # 退订成功通知
template_id_103 = "NuLtTyjF9-8pbWNOOEi2e7bjxgTFyOswWLfAJdYl-mA" # 乘客被动取消订单通知
