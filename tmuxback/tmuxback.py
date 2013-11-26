# -*- coding:utf-8 -*-
import util
import tmux_backup
import logging

if __name__ == '__main__':
    #TODO the log level should be read from user's config
    util.setup_log(logging.DEBUG, logging.DEBUG)
    tmux_backup.backup_tmux()
