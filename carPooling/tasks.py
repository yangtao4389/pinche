# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from app_weixin.settings import wx_map,logger

@shared_task
def aync_wx_template(template_id, touser, data, url=None, miniprogram=None, **kwargs):
    try:
        # logger.info("发送模板：template_id:%s,touser:%s,data:%s"%(template_id,touser,data))
        wx_map.template_send(template_id, touser, data, url, miniprogram, **kwargs)
    except:
        logger.exception("模板发送失败:template_id:%s,touser:%s,data:%s"%(template_id,touser,data))

