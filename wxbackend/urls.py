# -*- coding: utf-8 -*-
from django.conf.urls import url
from wxbackend import views,v_token_related,v_menu

urlpatterns = [
    url(r'^verifyToken$', v_token_related.verifyToken),  #
    # url(r'^getToken/$', v_token_related.getToken),  #
    # url(r"^wxbackend$",views.HandleExample),
    # url(r"^mediaHandle",views.mediaHandle),
    # url(r"^menuHandle",views.menuHandle),





    # url(r'^createMenu/$', v_menu.createMenu),  #
    # url(r'^callback.do/$', v_menu.createMenu),  #

]
