# -*- coding:utf-8 -*-
import subprocess
import re
import util


#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S:=:(#{session_width},#{session_height}):=:#{session_attached}'
CMD_LIST_WINDOWS='tmux list-windows -F#{window_index}:=:#{window_name}:=:#{window_active} -t%s'
#tmux list-panes -t {session}:{windowIdx}
CMD_LIST_PANES = 'tmux list-panes -t%s:%s -F#{pane_index}:=:(#{pane_width},#{pane_height}):=:#{pane_current_path}:=:#{pane_active}'

CMD_CREATE_SESSION='tmux new-session -d -s%s -n%s -x%d -y%d'

#capture pane content and save in given file. the first %s is paneIdstr, 2nd %s is filename
CMD_CAPTURE_PANE='tmux capture-pane -ep -t%s'

def get_sessions():
    """ 
    return a list of tmux session names:size:attached
    like: sessName:=:(200,300):=:1
    """
    cmd = CMD_LIST_SESSIONS.split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def get_windows_from_session(sess_name):
    """
    return a list of windows by given tmux session name
    like: 1:=:W-name:=:1
    idx:=:name:=:active
    """
    cmd = (CMD_LIST_WINDOWS % sess_name).split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')
    
def get_panes_from_sess_win(sess_name,win_idx):
    """return list of result string
      output format: paneIdx:=:(width,height):=:path:=:active
    """
    #dict parameter
    p = (sess_name,win_idx)
    cmd = (CMD_LIST_PANES % p).split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def capture_pane(pane_idstr,filename):
    """
    capture pane content and save in given filename.
    the format of pane_idstr is: sessionName:winIdx.paneIdx
    """
    cmd = (CMD_CAPTURE_PANE % pane_idstr).split(' ')
    util.exec_cmd_redir(cmd, filename)

def create_session(sess_name,win_name,width,height):
    p = (sess_name,win_name,width,height)
    cmd = (CMD_CREATE_SESSION % p).split(' ')
    s = util.exec_cmd(cmd)



if __name__ == '__main__':
    pass
