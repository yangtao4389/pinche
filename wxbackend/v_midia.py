import requests
from logging import getLogger
logger = getLogger("default")

class Media(object):
    # def __init__(self):
        # register_openers()
    #上传图片
    def uplaodOnce(self, accessToken, filePath, mediaType):
        param = {'media':  open(filePath, "rb")}
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (accessToken, mediaType)
        r = requests.post(postUrl, files=param)
        logger.info(r.content)
        return r.content


    #上传永久素材
    def uplaodForever(self, accessToken, filePath, mediaType):
        param = {'media':  open(filePath, "rb")}
        # postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=TYPE"
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (accessToken, mediaType)
        r = requests.post(postUrl, files=param)
        logger.info(r.content)
        return r.content