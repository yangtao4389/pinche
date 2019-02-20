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
from carPooling import views,api_home,error,api_userass

# 静态页面
urlpatterns = [
    url(r"^Home$", views.Home),
    url(r"^Home/Index$", views.Home),  #首页
    url(r"^Home/AssList$", views.AssList),  # 行程列表
    url(r"^Home/AssShareTip$", views.AssShareTip),  # 分享行程

    url(r"^UserAss/Publish$", views.UserAssPublish),  # 发布行程
    url(r"^UseAss/List$", views.UserAssList),   #  我的行程列表  我是车主
    url(r"^UserAss/Edit$", views.UserAssEdit),  #  车主行程编辑

    url(r"^UserRec/List$", views.UserRecList),  #  我的行程列表  我是乘客
    url(r"^UserCenter$", views.UserCenter),  #  个人中心


]


# ajax请求
urlpatterns += [
    url(r"^Home/GetCityList$", api_home.GetCityList),
    url(r"^Home/GetHotLine$", api_home.GetHotLine),
    url(r"^Home/GetCurTripTip$", api_home.GetCurTripTip),
    url(r"^Home/GetAssList$", api_home.GetAssList),
]

urlpatterns += [
    url(r"^UserAss/GetDetailData$", api_userass.GetDetailData), # 获取当前发布的数据
    url(r"^UserAss/GetLastAss$", api_userass.GetLastAss),  # 获取上一次的发布数据
    url(r"^UserAss/Cancel", api_userass.Cancel),  # 取消
    url(r"^UserAss/SaveEdit", api_userass.SaveEdit),  # 取消
]


# 错误信息
urlpatterns += [
    url(r"^Error/JsError$", error.JsError),
]
