#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       test.py
Last modified:  2014-05-22 23:11
Description:
    test the logger from logr
"""

import logr
import time

LOG_FILE_PATH = '/tmp/test.log'

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

class A(object):
    pass
a = A()
