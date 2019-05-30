"""sichuan_yd_children URL Configuration

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
from django.urls import path,include
from django.conf.urls import url
from django_app.settings import MEDIA_ROOT
from django.conf.urls.static import static
from carPooling.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^WebApp/", include('carPooling.urls')),
    url(r"^wxbackend/", include('app_weixin.urls')),


]
urlpatterns += static('/media/', document_root=MEDIA_ROOT)

urlpatterns += [
    # url(r"", Home)  # 所有未匹配的都跳到首页
]
from carPooling import views
from django.conf.urls import handler400, handler403, handler404, handler500
handler400=handler403=handler404=handler500=views.Home