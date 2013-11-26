# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import config
import datetime,time
import os,sys
from os import path 


LOG = util.get_logger()

WIN_BASE_IDX = tmux_cmd.get_option('base-index')
#PANE_BASE_IDX = tmux_cmd.get_option('pane-base-index')

def restore_tmux(tmux_id):
    """
    retore tmux sessions by given backuped Tmux id
    0 - read all backups from $HOME/.tmuxback/backup
    1 - if the given tmux_id is empty, take the latest
    2 - throw error msg if given name doesn't exist
    3 - check if there is tmux running and with same session name
    4 - handle windows, panes ..
    """
    #validate given tmux_id
    tmux_id = chk_tmux_id(tmux_id)

    LOG.info('loading backuped tmux sessions')
    LOG.debug('load json file:%s'% tmux_id + '.json' )

    tmux = util.json_to_obj(tmux_id)

    LOG.debug('converted json file to Tmux object')
    LOG.info('backuped tmux sessions loaded')
    
    for sess in  tmux.sessions:
        #check if session exists
        if tmux_cmd.has_session(sess.name):
            LOG.info('found session with same name in current tmux, \
                    skip restoring the session:%s.' % sess.name)
            continue
        restore_session(sess)


def restore_session(sess):
    """create the session from session object"""
    tmux_cmd.create_session(sess.name,sess.size)
    for win in sess.windows_in_reverse()[:-1]:
        #rename, renumber window
        restore_window(sess.name, win)
        tmux_cmd.create_empty_window(sess.name, WIN_BASE_IDX)

    # the last window
        restore_window(sess.name, sess.windows_in_reverse()[-1])


def restore_window(win):
    LOG.info('restoring window: %' % win.sess_name+':'+win.win_id)
    #renumber from base_index to backuped index
    tmux_cmd.renumber_window(win.sess_name, WIN_BASE_IDX, win.win_id)
    #rename win
    tmux_cmd.rename_window(win.sess_name,win.win_id)
    
    #select window (active)
    if win.active:
        tmux_cmd.active_window(win.sess_name,win_id)

    if len(win.panes) >1 :
        #multiple panes
        #split
        for i in range(len(win.panes)-1):
            tmux_cmd.split_window(win.sess_name,window,win.min_pane_id())

    for p in win.panes:
        restore_pane(p)

    #set layout
    tmux_cmd.select_layout(sess_name,win.win_id,win.layout)

def restore_pane(pane):
    LOG.info('restoring pane: %'% pane.idstr())
    #set path
    tmux_cmd.set_pane_path(pane.idstr(), pane.path)
    # restore content


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

