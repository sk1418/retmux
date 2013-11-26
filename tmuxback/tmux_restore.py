# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import config
import datetime,time
import os,sys
from os import path 


LOG = util.get_logger()

def restore_tmux(tmux_id):
    """
    retore tmux sessions by given backuped Tmux id
    0 - read all backups from $HOME/.tmuxback/backup
    1 - if the given tmux_id is empty, take the latest
    2 - throw error msg if given name doesn't exist
    3 - check if there is tmux running and with same session name
    4 - handle windows, panes ..
    """
    tmux_id = chk_tmux_id(tmux_id)
    LOG.info('loading backuped tmux sessions')
    LOG.debug('load json file:%s'% tmux_id + '.json' )
    tmux = util.json_to_obj(tmux_id)
    LOG.debug('converted json file to Tmux object')
    LOG.info('backuped tmux sessions loaded')

    


def chk_tmux_id(tmux_id):
    """check the tmux_id (backup name)"""
    #if no backup exists, exit application
    all_bk =util.all_backups() 
    if len(all_bk)<1:
        LOG.error('backup dir is empty, nothing to restore')
        sys.exit(1)

    #checking tmux_id
    if tmux_id:
        if not all_bk.__contains__(tmux_id):
            LOG.error('cannot find given backup name')
            sys.exit(1)
    else:
        tmux_id = util.latest_backup()
        LOG.info('backup name is empty, using last backup:%s'%tmux_id)

    return tmux_id

def chk_session_exists(sess_name):
    """check if session name exists in current tmux"""
    pass
