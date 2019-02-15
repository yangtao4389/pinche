import time,datetime,os
class UIDMaker:
    """
    uid生成器
    """

    def __init__(self, prefix=""):
        """
        @parame prefix: uid前缀字符串
        """
        self.prefix = prefix
        self.prepStr = prefix + "%s" + "%05u" % os.getpid() + "%05u"
        self.noPrefixStr = "%s" + "%05u" % os.getpid() + "%05u"
        self._auto_id = 0    # 局计数，0xFFFF一轮回

    def make(self, matchStr):
        """
        make new id
        """
        t = time.time()
        st = time.strftime("%Y%m%d%H%M%S", time.localtime(t)) + "%03d" % int(t * 1000 % 1000)
        self._auto_id = self._auto_id % 0xFFFF + 1
        return matchStr % ( st, self._auto_id )

    def __call__(self):
        """
        @return: string
        201101010000001111100000
        """
        return self.make(self.prepStr)

    def asNoPrefix(self):
        """
        输出没有 prefix 的uid
        """
        return self.make(self.noPrefixStr)


class UIDMaker_DateTime:
    """
    uid生成器
    """

    def __init__(self, prefix=""):
        """
        @parame prefix: uid前缀字符串
        """
        self.prefix = prefix

    def __call__(self):
        """
        @return: string
        """
        return self.prefix + self.asNoPrefix()

    def asNoPrefix(self):
        """
        输出没有 prefix 的uid
        1325815959781
        """
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


class UIDMaker_TimeOnly:
    """
    uid生成器
    """

    def __init__(self, prefix=""):
        """
        @parame prefix: uid前缀字符串
        """
        self.prefix = prefix

    def __call__(self):
        """
        @return: string
        """
        return self.prefix + self.asNoPrefix()

    def asNoPrefix(self):
        """
        输出没有 prefix 的uid
        1325815959781
        """
        return str(time.time() * 1000)

UIDMaker_DateTime_obj = UIDMaker_DateTime()