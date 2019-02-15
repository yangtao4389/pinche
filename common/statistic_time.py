import time
from functools import wraps
from logging import getLogger
logger = getLogger("default")


def decorate_time_consuming(fn):
    '''
    统计函数执行时间装饰器，会存入到日志文件中
    '''
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        start = time.clock()
        ret = fn(*args, **kwargs)
        logger.info("%s cost %s second"%(fn.__name__, time.clock() - start))
        return ret
    return _wrapper
