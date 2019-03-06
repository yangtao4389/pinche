from logging import getLogger
from . import receive,reply
from django.shortcuts import HttpResponse

logger = getLogger("default")


def xml_text(request):

    try:
        webData = request.body
        logger.info("post请求的数据request.body：%s" % webData)
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            # content = "test"
            # replyMsg = reply.TextMsg(toUser, fromUser, content)
            # return replyMsg.send()
            if recMsg.MsgType == 'text':
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            if recMsg.MsgType == 'image':
                mediaId = recMsg.MediaId
                logger.info("MediaId:%s"%mediaId)
                replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                return replyMsg.send()
            else:
                return reply.Msg().send()
        else:
            return "success"
    except:
        logger.exception("处理post数据出错")
        return "success"
