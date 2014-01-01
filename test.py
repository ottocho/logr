#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       test.py
Last modified:  2014-01-01 17:36
Description:
    test the logger from logr
"""

import logr
import time

LOG_FILE_PATH = '/tmp/test'

logger = logr.get_logger('test', LOG_FILE_PATH)
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
