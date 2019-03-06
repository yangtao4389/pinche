# from weixin.client import WeixinAPI
# from weixin.oauth2 import OAuth2AuthExchangeError

APPID = "wxd2ee708e2f14a707"
APPSECRET = "7ea2c0df5e192baa3565bb0b6bed4cc7"
REDIRECT_URI = 'https://passport.yhd.com/wechat/callback.do'


code = 'zklLeXQ1GNbspMgRQ5XhZpAke5UsVT0sEFECvcDRq8s'

from py3weixin.client import WeixinMpAPI

scope = ("snsapi_base", )
api = WeixinMpAPI(appid=APPID,
                  app_secret=APPSECRET,
                  redirect_uri=REDIRECT_URI)
authorize_url = api.get_authorize_url(scope=scope)

access_token = api.exchange_code_for_access_token(code=code)

api = WeixinMpAPI(access_token=access_token)

user = api.user(openid="openid")