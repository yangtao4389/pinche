# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from py_modules.werobot.contrib.django import make_view
from .views import myrobot

urlpatterns = [


    url(r"^passiveMsg$", make_view(myrobot)), #GET验证verifyToken，POST为被动消息


    # url(r"^verifyTokenOrpassiveMsg", weixin.django_view_func()),
    # url(r"^wxbackend$",views.HandleExample),
    # url(r"^mediaHandle",views.mediaHandle),
    # url(r"^menuHandle",views.menuHandle),





    # url(r'^createMenu/$', v_menu.createMenu),  #
    # url(r'^callback.do/$', v_menu.createMenu),  #

]
