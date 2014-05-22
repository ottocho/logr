#!/usr/bin/env python
#coding:utf8

"""
Author:         ottocho
Filename:       logr.py
Last modified:  2014-05-22 23:35
Description:
    a simple logger

    mainly from tornado
    * simplfy the formatter from tornado.log
    * define the new line format(add the code location infomation)
"""

import os
import sys
import time
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler

try:
    import curses
except ImportError:
    curses = None

__all__ = [ 'get_logger' ]

if type('') is not type(b''):
    bytes_type = bytes
    unicode_type = str
    basestring_type = str
else:
    bytes_type = str
    unicode_type = unicode
    basestring_type = basestring

_TO_UNICODE_TYPES = (unicode_type, type(None))

def _stderr_supports_color():
    color = False
    if curses and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color

def to_unicode(value):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    assert isinstance(value, bytes_type), \
        "Expected bytes, unicode, or None; got %r" % type(value)
    return value.decode("utf-8")

# to_unicode was previously named _unicode not because it was private,
# but to avoid conflicts with the built-in unicode() function/type
_unicode = to_unicode

class LogFormatter(logging.Formatter):
    """Log formatter used in Tornado.

    Key features of this formatter are:

    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.

    """
    def __init__(self, color=True, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self._color = color and _stderr_supports_color()
        if self._color:
            # The curses module has some str/bytes confusion in
            # python3.  Until version 3.2.3, most methods return
            # bytes, but only accept strings.  In addition, we want to
            # output these strings with the logging module, which
            # works with unicode strings.  The explicit calls to
            # unicode() below are harmless in python2 but will do the
            # right conversion in python 3.
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = unicode_type(fg_color, "ascii")
            self._colors = {
                logging.DEBUG: unicode_type(curses.tparm(fg_color, 4),  # Blue
                                            "ascii"),
                logging.INFO: unicode_type(curses.tparm(fg_color, 2),  # Green
                                           "ascii"),
                logging.WARNING: unicode_type(curses.tparm(fg_color, 3),  # Yellow
                                              "ascii"),
                logging.ERROR: unicode_type(curses.tparm(fg_color, 1),  # Red
                                            "ascii"),
            }
            self._normal = unicode_type(curses.tigetstr("sgr0"), "ascii")

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)
        assert isinstance(record.message, basestring_type)  # guaranteed by logging
        record.asctime = time.strftime(
            "%Y-%m-%d %H:%M:%S", self.converter(record.created))

        prefix = '%(name)-12s %(asctime)s %(levelname)-8s (%(filename)s:%(lineno)d)' \
                    % record.__dict__
        _func_name = record.__dict__['funcName']
        if _func_name != '<module>':
            _func_name += '()'
        prefix += ':' + _func_name

        if self._color:
            prefix = (self._colors.get(record.levelno, self._normal) +
                      prefix + self._normal)

        # Encoding notes:  The logging module prefers to work with character
        # strings, but only enforces that log messages are instances of
        # basestring.  In python 2, non-ascii bytestrings will make
        # their way through the logging framework until they blow up with
        # an unhelpful decoding error (with this formatter it happens
        # when we attach the prefix, but there are other opportunities for
        # exceptions further along in the framework).
        #
        # If a byte string makes it this far, convert it to unicode to
        # ensure it will make it out to the logs.  Use repr() as a fallback
        # to ensure that all byte strings can be converted successfully,
        # but don't do it by default so we don't add extra quotes to ascii
        # bytestrings.  This is a bit of a hacky place to do this, but
        # it's worth it since the encoding errors that would otherwise
        # result are so useless (and tornado is fond of using utf8-encoded
        # byte strings whereever possible).
        def safe_unicode(s):
            try:
                return _unicode(s)
            except UnicodeDecodeError:
                return repr(s)

        formatted = prefix + " " + safe_unicode(record.message)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(safe_unicode(ln) for ln in record.exc_text.split('\n'))
            formatted = '\n'.join(lines)
        return formatted.replace("\n", "\n    ")

def get_logger(logger_name, log_file_path, log_level=logging.DEBUG):
    '''Get the logger which:

    * well-formatted
    * colorized
    * with code location
    * daily-rotated

    :param logger_name: name of the logger
    :param log_file_path: full path of the log
    :param log_level: level of the log

    '''
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if len(logger.handlers) == 0:
        rotating_file_handler = TimedRotatingFileHandler(log_file_path, 'D', 1, 0)
        rotating_file_handler.suffix = "%Y%m%d.%H%M%S.log"
        rotating_file_handler.setFormatter(LogFormatter(color=True))
        logger.addHandler(rotating_file_handler)
    return logger

