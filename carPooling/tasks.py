# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from app_weixin.settings import wx_map,logger

@shared_task
def aync_wx_template(template_id, touser, data, url=None, miniprogram=None, **kwargs):
    try:
        wx_map.template_send(template_id, touser, data, url, miniprogram, **kwargs)
    except:
        logger.exception("模板发送失败")

