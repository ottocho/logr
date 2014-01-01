#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       logr.py
Last modified:  2014-01-01 17:42
Description:    a simple logger
"""

import os
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

__all__ = [ 'get_logger' ]

def _get_file_handler(logger_name, log_file_path):
    '''
        Get the time-rotating filehandler.
        The handler writes logs on file `log_file_path`, rotates it daily.

        `logger_name`: name of the logger
        `log_file_path`: full path of the log
    '''
    rotating_file_handler = TimedRotatingFileHandler(log_file_path, 'D', 1, 0)
    rotating_file_handler.suffix = "%Y%m%d.%H%M%S.log"
    log_format = '%(name)-12s %(asctime)s %(levelname)-8s %(message)s'
    time_format = '%Y-%m-%d %H:%M:%S'
    log_formatter = logging.Formatter(log_format, time_format)
    rotating_file_handler.setFormatter(log_formatter)
    return rotating_file_handler

class LocationLogger(logging.LoggerAdapter):
    """ logging with code location """
    def process(self, msg, kwargs):
        location = ''
        func_name = ''
        traced_stacks = traceback.extract_stack()
        if len(traced_stacks) > 2:
            _name = os.path.basename(traced_stacks[-3][0])
            _line_number = traced_stacks[-3][1]
            location = '(%s:%d):' % (_name, _line_number)
            func_name = traced_stacks[-3][2]
            if func_name != '<module>':
                func_name += '()'
        mmsg = '%s%s - %s' % (location, func_name, msg)
        return mmsg, kwargs

def get_logger(logger_name, log_file_path, log_level=logging.DEBUG):
    ''' get the logger
        logging with code location
        rotate the log daily

        `logger_name`: name of the logger
        `log_file_path`: full path of the log
        `log_level`: level of the log
    '''
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if len(logger.handlers) == 0:
        rotating_file_handler = _get_file_handler(logger_name, log_file_path)
        logger.addHandler(rotating_file_handler)
    return LocationLogger(logger, {})
