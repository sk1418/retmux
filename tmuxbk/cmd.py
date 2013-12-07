# -*- coding:utf-8 -*-
import subprocess
import re
import util
import log

LOG = log.get_logger()

#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S:=:(#{session_width},#{session_height}):=:#{session_attached}'
#tmux list-panes -t {session}:{windowIdx}
CMD_LIST_PANES = 'tmux list-panes -t%s:%s -F#{pane_index}:=:(#{pane_width},#{pane_height}):=:#{pane_current_path}:=:#{pane_active}'

CMD_CREATE_SESSION='tmux new-session -d -s%s -x%d -y%d'

#capture pane content and save in given file. the first %s is paneIdstr, 2nd %s is filename
CMD_CAPTURE_PANE='tmux capture-pane -ep -t%s'
CMD_SHOW_OPTION='tmux show-options -gv %s'
CMD_HAS_SESSION='tmux has-session -t%s'
CMD_SET_PANE_PATH='tmux send-keys -t%s cd \"%s\"\nclear\n'

CMD_LIST_WINDOWS='tmux list-windows -F#{window_index}:=:#{window_name}:=:#{window_active}:=:#{window_layout} -t%s'
CMD_MOVE_WINDOW='tmux move-window -s%s -t%s'
CMD_RENAME_WINDOW='tmux rename-window -t%s:%d %s'
CMD_NEW_EMPTY_WINDOW='tmux new-window -d -t%s:%d'
CMD_ACTIVE_WINDOW = 'tmux select-window -t%s:%d'
CMD_SPLIT_WINDOW = 'tmux split-window -d -t%s:%d.%d'
CMD_SET_LAYOUT = 'tmux select-layout -t%s:%d %s'
CMD_LOAD_CONTENT = 'tmux send-keys -t%s cat %s\n'

def has_tmux_server():
    cmd = CMD_LIST_SESSIONS.split(' ')
    code = util.cmd_return_code(cmd)
    return code == 0

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

def set_pane_path(pane_idstr, path):
    """ set pane path by 'send-key' and clear the screen"""
    cmd = (CMD_SET_PANE_PATH % (pane_idstr,path)).split(' ',3)
    util.exec_cmd(cmd)


def capture_pane(pane_idstr,filename):
    """
    capture pane content and save in given filename.
    the format of pane_idstr is: sessionName:winIdx.paneIdx
    """
    cmd = (CMD_CAPTURE_PANE % pane_idstr).split(' ')
    util.exec_cmd_redir(cmd, filename)

def create_session(sess_name,size):
    p = (sess_name,size[0],size[1])
    cmd = (CMD_CREATE_SESSION % p).split(' ')
    s = util.exec_cmd(cmd)

def create_empty_window(sess_name, base_index):
    p = (sess_name, int(base_index))
    cmd = (CMD_NEW_EMPTY_WINDOW % p).split(' ')
    util.exec_cmd(cmd)

def split_window(sess_name, win_id, pane_min_id):
    p = (sess_name,int(win_id), int(pane_min_id))
    cmd = (CMD_SPLIT_WINDOW % p).split(' ')
    util.exec_cmd(cmd)

def active_window(sess_name, win_id):
    p = (sess_name,win_id)
    cmd = (CMD_ACTIVE_WINDOW% p).split(' ')
    util.exec_cmd(cmd)

def select_layout(sess_name, win_id, layout):
    p = (sess_name,win_id,layout)
    cmd = (CMD_SET_LAYOUT% p).split(' ')
    util.exec_cmd(cmd)

def rename_window(sess_name, win_id, name):
    """
    rename the window in session
    """
    p = (sess_name, win_id, name)
    cmd = (CMD_RENAME_WINDOW % p).split(' ')
    util.exec_cmd(cmd)

def renumber_window(sess_name, win_id_from, win_id_to):
    """
    renumber the window in session
    """
    p = (sess_name  + ':' + str(win_id_from), \
        sess_name + ':' + str(win_id_to))

    cmd = (CMD_MOVE_WINDOW % p).split(' ')
    util.exec_cmd(cmd)

def get_option(option):
    """ get global option value """
    cmd = (CMD_SHOW_OPTION % option).split(' ')
    return  util.exec_cmd(cmd)
    
def has_session(sess_name):
    """check if a session exists already"""
    cmd = (CMD_HAS_SESSION%sess_name).split(' ')
    return util.cmd_return_code(cmd) == 0

def restore_pane_content(pane_idstr,filename):
    """restore backuped pane content. This is done in two
    steps, 
    1: load buffer from file
    2: paste buffer
    """
    cmd = (CMD_LOAD_CONTENT %  (pane_idstr,filename)).split(' ',3)
    util.exec_cmd(cmd)
