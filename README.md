logger
======

We always need(or must) write log. But I am sick about config the logging time and time again.

the function `get_logger` return the logger which logs on file `log_path/logger_name`, and rotates it daily.

Usage:

    from logger import *
    import time

    LOG_DIR = '/home/ottocho/log/'

    logger = get_logger('test', LOG_DIR)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')

    class AClass():
       def a_method(self):
           logger.debug('call a_method()')

    def error_devide():
       try:
           1/0
       except:
           logger.error('in exception', exc_info=True)

    aobj = AClass()
    aobj.a_method()
    error_devide()
