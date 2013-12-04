# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import config
import datetime,time
import os
from os import path 

LOG = util.get_logger()

#FIXME here we need a parameter "name", same idea as restore, if name is empty,
# use default name. name should be uniq too, (check needed)
def backup_tmux():
    """get current tmux information and return Tmux object"""
    LOG.info('backing up the current tmux sessions')
    #id is timestamp
    tmux_id = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    parent_dir    = path.join(config.BACKUP_PATH,tmux_id)

    tmux          = tmux_obj.Tmux(tmux_id)
    tmux.sessions = load_sessions()

    util.to_json(tmux, parent_dir, tmux_id + '.json')

    #if tmux and not os.path.exists(parent_dir):
        #os.makedirs(parent_dir)
    for s in tmux.sessions:
        for w in s.windows:
            for p in w.panes:
                tmux_cmd.capture_pane(p.idstr(), path.join(parent_dir,p.idstr()))

    LOG.info('Backup of sessions are saved under %s'%parent_dir)

def load_sessions():
    """load sessions information """
    LOG.debug('Backup sessions')
    output = tmux_cmd.get_sessions()
    sess = []

    #FIXME If no session, no backup., the output parsing part need to be fixed.
    for s in output:
        #s is like  sessName:(200,300):1
        s_l = s.split(config.SEP)
        session =tmux_obj.Session(s_l[0]) 
        session.size = eval(s_l[1])
        session.attached = int(s_l[2])>0
        #load windows
        session.windows = load_windows(session.name)
        sess.append(session)
    return sess

def load_windows(s_name):
    """load windows for given session name"""
    LOG.debug('Backup windows of session %s'%s_name)
    output = tmux_cmd.get_windows_from_session(s_name)
    wins = []
    for s in output:
        #s is like 1:wname:1
        w_l = s.split(config.SEP)
        win = tmux_obj.Window(s_name,int(w_l[0]))
        win.name = w_l[1]
        win.active = int(w_l[2])
        win.layout = w_l[3]
        #load panes
        win.panes = load_panes(s_name,win.win_id)

        wins.append(win)
    return wins
        

def load_panes(s_name,w_id):
    """
    load panes for given session name and window idx
    """
    LOG.debug('Backup panes of window: %s:%d'%(s_name,w_id))
    output = tmux_cmd.get_panes_from_sess_win(s_name,w_id)
    panes = []
    for s in output:
        #output format: paneIdx:=:width:=:height:=:path:=:active
        p_l = s.split(config.SEP)
        pane = tmux_obj.Pane(s_name,w_id,int(p_l[0]))
        pane.size = eval(p_l[1])
        pane.path = p_l[2]
        pane.active = int(p_l[3])
        panes.append(pane)
    return panes

