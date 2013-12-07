#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       logger.py
Last modified:  2013-12-07 23:52
Description:    a simple logger
"""

import os
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

__all__ = [ 'get_logger' ]

def get_file_handler(logger_name, log_path):
    '''
        Get the time-rotating filehandler.
        The handler writes logs on file `log_path/logger_name`, rotates it daily.

        `logger_name`: name of the logger
        `log_path`: location of the logs
    '''
    log_path = os.path.join(log_path, logger_name)
    rotating_file_handler = TimedRotatingFileHandler(log_path, 'D', 1, 0)
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

def get_logger(logger_name, log_path, log_level=logging.DEBUG):
    ''' get the logger
        logging with code location
        rotate the log daily

        `logger_name`: name of the logger
        `log_path`: location of the logs
        `log_level`: level of the log
    '''
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if len(logger.handlers) == 0:
        rotating_file_handler = get_file_handler(logger_name, log_path)
        logger.addHandler(rotating_file_handler)
    return LocationLogger(logger, {})
