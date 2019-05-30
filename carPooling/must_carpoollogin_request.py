from re import compile
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from common import client
from app_weixin.settings import wx_map


from logging import getLogger
logger = getLogger("default")


extra_urls = ["/WebApp/Home/WeixinLogin","/WebApp/Home/WeiXinLoginCallBack","/WebApp/Home/WeiXinSubscrible"]
# 有些接口不用验证
extra_urls += ["/WebApp/lunxun/msg_polling"]
# extra_urls += ["/WebApp/Home","/WebApp/Home/AssList"]

must_login_urls = [
    (r'/WebApp/*'),
]



must_login_urls_compile = [compile(expr) for expr in must_login_urls]

class MustCarpoolloginRequest(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        # 实现微信登录
        if any(m.match(path) for m in must_login_urls_compile) and path not in extra_urls:
            logger.info("MustCarpoolloginRequest:每一次进入的url记录：%s" % client.get_client_current_full_path(request))
            # request.session["w_openid"] = "oSczv05h7ZJ6KISCTfOeZ3SOel2M"  # 发布用户
            # request.session["w_openid"] = "11111122222222"  # 预定用户
            # request.session["w_openid"] = "moniyognhu"  # 预定用户
            # request.session["w_openid"] =None # 预定用户
            w_openid = request.session.get('w_openid')
            logger.info("session中用户id：%s" % (w_openid))
            # if not w_openid:
            #     request.session["tmp_current_full_url"] = client.get_client_current_full_path(request)
            #     return HttpResponseRedirect(extra_urls[0])

            # 判断是否关注公众号
            # if request.session.get(WSUBSCRIBE) != 1:
            #     # 这里可以直接跳转到关注页面
            #     try:
            #         result = wx_map.user_info(w_openid)
            #         logger.info("关注：result:%s"%result)
            #         if result.subscribe == 1:
            #             request.session[WSUBSCRIBE] = 1
            #         else:
            #             raise Exception()
            #     except:
            #         return HttpResponseRedirect(DEFAULT_Subscrible_FULL_PATH)
                    # return HttpResponseRedirect("https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI4MTU5NzAzOQ==&scene=124#wechat_redirect")
                    # return HttpResponseRedirect("https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU1NTcwNzk3Nw==&scene=123#wechat_redirect")


