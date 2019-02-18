"""sichuan_yd_video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls import url
from carPooling import views,api,error

# 静态页面
urlpatterns = [
    url(r"^Home$", views.Home),
    url(r"^Home/Index$", views.Home),
    url(r"^Home/AssList$", views.AssList),
]


# ajax请求
urlpatterns += [
    url(r"^Home/GetCityList$", api.GetCityList),
    url(r"^Home/GetHotLine$", api.GetHotLine),
    url(r"^Home/GetCurTripTip$", api.GetCurTripTip),

]

# 错误信息
urlpatterns += [
    url(r"^Error/JsError$", error.JsError),
]
