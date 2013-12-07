# -*- coding:utf-8 -*-
import util
import cmd
import tmux_obj
import log
import config
import datetime,time
import os,sys
from os import path 


LOG = log.get_logger()

WIN_BASE_IDX = int(cmd.get_option('base-index'))
#PANE_BASE_IDX = cmd.get_option('pane-base-index')

def restore_tmux(tmux_id):
    """
    retore tmux sessions by given backuped Tmux id
     - check if there is tmux running and with same session name
     - handle windows, panes ..
    """
    #validate given tmux_id
    LOG.info('loading backuped tmux sessions')
    jsonfile = os.path.join(config.BACKUP_PATH,tmux_id,tmux_id+'.json')
    LOG.debug('load json file:%s'% jsonfile )

    tmux = util.json_to_obj(jsonfile)
    LOG.debug('converted json file to Tmux object')
    LOG.info('backuped tmux sessions loaded')
    
    for sess in  tmux.sessions:
        LOG.debug('processing session name %s'%sess.name)
        #check if session exists
        if cmd.has_tmux_server() and cmd.has_session(sess.name):
            LOG.info('found session with same name in current tmux, \
skip restoring the session:%s.' % sess.name)
            continue
        restore_session(sess, tmux_id)


def restore_session(sess, tmux_id):
    """create the session from session object"""
    LOG.debug('create session, with initial win: %s' % sess.name)
    cmd.create_session(sess.name,sess.size)
    for win in sess.windows_in_reverse()[:-1]:
        #rename, renumber window
        restore_window(win, tmux_id)

        LOG.debug('create empty window with baseIdx: %s' % WIN_BASE_IDX)
        cmd.create_empty_window(sess.name, WIN_BASE_IDX)

    # the last window
    restore_window(sess.windows_in_reverse()[-1], tmux_id)


def restore_window(win, tmux_id):
    LOG.info('restoring window: %s' % win.sess_name+':'+str(win.win_id))
    #renumber from base_index to backuped index
    if WIN_BASE_IDX != win.win_id:
        cmd.renumber_window(win.sess_name, WIN_BASE_IDX, win.win_id)
    #rename win
    cmd.rename_window(win.sess_name,win.win_id,win.name)
    
    #select window (active)
    if win.active:
        cmd.active_window(win.sess_name,win.win_id)

    if len(win.panes) >1 :
        #multiple panes
        #split
        for i in range(len(win.panes)-1):
            cmd.split_window(win.sess_name,win.win_id,win.min_pane_id())

    for p in win.panes:
        restore_pane(p, tmux_id)

    #set layout
    cmd.select_layout(win.sess_name, win.win_id, win.layout)

def restore_pane(pane, tmux_id):
    LOG.info('restoring pane: %s'% pane.idstr())
    #set path
    cmd.set_pane_path(pane.idstr(), pane.path)

    #restore content
    filename = os.path.join(config.BACKUP_PATH,tmux_id,pane.idstr())

    cmd.restore_pane_content(pane.idstr(), filename)

