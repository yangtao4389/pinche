# -*- coding: utf-8 -*-
from django.conf.urls import url
from wxbackend import views,v_token_related,v_menu
from weixinLibrary import Weixin
config = dict(
    WEIXIN_APP_ID='wx7b27955ce810b11f',
    WEIXIN_APP_SECRET='d2754228e5db08f3ce1a1011d59e9798',
    WEIXIN_TOKEN="HELLOWORLD",
)
weixin = Weixin(config)
from weixinLibrary.msg import WeixinMsg
msg = WeixinMsg("e10adc3949ba59abbe56e057f20f883e", None, 0)
@msg.all
def all_test(**kwargs):
    print(kwargs)
    # 或者直接返回
    # return "all"
    return msg.reply(
        kwargs['sender'], sender=kwargs['receiver'], content='all'
    )

@msg.text()
def hello(**kwargs):
    return dict(content="hello too!", type="text")

urlpatterns = [
    # url(r'^passiveMsg$', v_token_related.verifyToken),  #
    url(r'^getToken$', v_token_related.getToken),  #
    url(r"^passiveMsg$", weixin.django_view_func()), #GET验证verifyToken，POST为被动消息
    # url(r"^verifyTokenOrpassiveMsg", weixin.django_view_func()),
    # url(r"^wxbackend$",views.HandleExample),
    # url(r"^mediaHandle",views.mediaHandle),
    # url(r"^menuHandle",views.menuHandle),





    # url(r'^createMenu/$', v_menu.createMenu),  #
    # url(r'^callback.do/$', v_menu.createMenu),  #

]
