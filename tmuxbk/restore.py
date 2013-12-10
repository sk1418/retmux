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

WIN_BASE_IDX = None

#in case there is no tmux session, create a new dummy session, need to be removed at the end
DUMMY_SESSION = None 

#PANE_BASE_IDX = cmd.get_option('pane-base-index')

def win_base_idx():
    """get the tmux's win-base-idx option, if no server was started, create a 
    dummy session, the session needs to be removed after restoring"""

    global WIN_BASE_IDX
    if WIN_BASE_IDX == None:
        if not cmd.has_tmux_server():
            global DUMMY_SESSION
            DUMMY_SESSION = util.random_str(10)
            LOG.debug('Create Dummy session:%s'%DUMMY_SESSION)
            cmd.create_session(DUMMY_SESSION, '[10,10]')
        WIN_BASE_IDX = int(cmd.get_option('base-index'))
    return WIN_BASE_IDX


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
            LOG.warning('found session with same name in current tmux, \
skip restoring the session:%s.' % sess.name)
            continue
        restore_session(sess, tmux_id)

    LOG.debug('check and kill dummy session')
    if DUMMY_SESSION:
        cmd.kill_session(DUMMY_SESSION)
    LOG.info('Backup %s is restored! run "tmux list-sessions" to see sessions and attach'% tmux_id)

def restore_session(sess, tmux_id):
    """create the session from session object"""
    LOG.debug('create session, with initial win: %s' % sess.name)
    cmd.create_session(sess.name,sess.size)
    for win in sess.windows_in_reverse()[:-1]:
        #rename, renumber window
        restore_window(win, tmux_id)

        LOG.debug('create empty window with baseIdx: %s' % win_base_idx())
        cmd.create_empty_window(sess.name, win_base_idx())

    # the last window
    restore_window(sess.windows_in_reverse()[-1], tmux_id)


def restore_window(win, tmux_id):
    LOG.info('restoring window: %s' % win.sess_name+':'+str(win.win_id))
    #renumber from base_index to backuped index
    if win_base_idx() != win.win_id:
        cmd.renumber_window(win.sess_name, win_base_idx(), win.win_id)
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

