# -*- coding:utf-8 -*-
import subprocess
import re
import util


#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S:=:[#{session_width},#{session_height}]:=:#{session_attached}'
CMD_LIST_WINDOWS='tmux list-windows -F#{window_index}:=:#{window_name}:=:#{window_active} -t%s'
#tmux list-panes -t {session}:{windowIdx}
CMD_LIST_PANES='tmux list-panes -t%s:%s -F#{window_index}:=:#{window_name}'

CMD_CREATE_SESSION='tmux new-session -d -s%s -n%s -x%d -y%d'

def get_sessions():
    """ 
    return a list of tmux session names:size:attached
    like: sessName:[200,300]:1
    """
    cmd = CMD_LIST_SESSIONS.split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def get_windows_from_session(sess_name):
    """
    return a list of windows by given tmux session name
    like: 1:W-name:1
    idx:name:active
    """
    cmd = (CMD_LIST_WINDOWS % sess_name).split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')
    
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
