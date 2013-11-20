# -*- coding:utf-8 -*-
import subprocess
import re
import util


#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S'
CMD_LIST_WINDOWS='tmux list-windows -F#{window_index}:#{window_name} -t(sess_name)s'
#tmux list-panes -t {session}:{windowIdx}
CMD_LIST_PANES='tmux list-panes -t%s:%s -F#{window_index}:#{window_name}'

CMD_CREATE_SESSION='tmux new-session -d -s%s -n%s -x%d -y%d'

def get_session_names():
    """ return a list of tmux session names """
    cmd = CMD_LIST_SESSIONS.split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def get_windows_from_session(sess_name):
    """return a dict {index:win_name} of windows by given session"""
    cmd = (CMD_LIST_WINDOWS % sess_name).split(' ')
    s = util.exec_cmd(cmd)
    l = s.split('\n')
    return dict(x.split(':') for x in l)
    
def get_panes_from_sess_win(sess_name,win_idx):
    """return list of result string"""
    #dict parameter
    p = (sess_name,win_idx)
    cmd = (CMD_LIST_PANES % p).split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def create_session(sess_name,win_name,width,height):
    p = (sess_name,win_name,width,height)
    cmd = (CMD_CREATE_SESSION % p).split(' ')
    s = util.exec_cmd(cmd)



if __name__ == '__main__':
    pass
