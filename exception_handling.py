import functools
import logging
from sendEmail import SendEmail
import traceback

def create_logger():
    logger = logging.getLogger("xvideos_log")
    logger.setLevel(logging.INFO)
    if not logger.handlers:    
        fh = logging.FileHandler("xvideos.log")
        fmt = "[%(asctime)s-%(name)s-%(levelname)s]:\n%(message)s"
        formatter = logging.Formatter(fmt)    #设置格式
        fh.setFormatter(formatter)    #将相应的handler添加在logger对象中
        logger.addHandler(fh)    #打印日记
        #logger.removeHandler(fh)    #在记录日志之后移除句柄，以解决 logging 重复写日志问题
    return logger

def log_exception(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            fn(*args, **kwargs)
        except Exception as e:
            SendEmail(traceback.format_exc())
            logger.exception("[Error in {}] msg: {}".format(__name__, str(e)))
            with open('xvideos.log','a+',encoding='utf-8') as f:
                f.write('\n')
            raise    #主动抛出异常
    return wrapper