# -*- coding:utf-8 -*-
import logging
import os
import config

class TmuxbackFormatter(logging.Formatter):
    """define different format for different log levels"""

    err_fmt  = "ERROR: %(msg)s"
    dbg_fmt  = "DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "%(msg)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = TmuxbackFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = TmuxbackFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = TmuxbackFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result

def setup_log(console_lvl, file_lvl):
    """setup_log, this function should be called only once at the beginning of application starts"""
    logger = logging.getLogger('tmuxbackLogger')
    logger.setLevel(file_lvl)

    # create file handler which logs even debug messages
    fh = logging.handlers.RotatingFileHandler(\
            os.path.join(config.USER_PATH,'tmuxback.log'), \
           maxBytes=5000000, backupCount=5 )
    fh.setLevel(file_lvl)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(console_lvl)

    # create formatter and add it to the handlers
    fhFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    chFormatter = TmuxbackFormatter()

    fh.setFormatter(fhFormatter)
    ch.setFormatter(chFormatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.debug("Log system setup successfully")

def get_logger():
    return logging.getLogger('tmuxbackLogger')
