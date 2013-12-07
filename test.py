#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       test.py
Last modified:  2013-12-07 23:58
Description:
    test the logger

"""

from logger import *
import time

LOG_DIR = '/tmp/'

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
