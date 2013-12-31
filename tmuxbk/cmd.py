# -*- coding:utf-8 -*-
import subprocess
import re
import util
import log
import config

LOG = log.get_logger()

#tmux commands

##list sessions

CMD_LIST_SESSIONS    = config.CMD_SEP.join(['tmux', 'list-sessions', '-F#S:=:(#{session_width},#{session_height}):=:#{session_attached}'])
#tmux list-panes -t {session}:{windowIdx}
CMD_LIST_PANES       = config.CMD_SEP.join(['tmux','list-panes','-t%s:%s', '-F#{pane_index}:=:(#{pane_width},#{pane_height}):=:#{pane_current_path}:=:#{pane_active}'])
CMD_CREATE_SESSION   = config.CMD_SEP.join(['tmux','new-session', '-d','-s%s','-x%d','-y%d'])
CMD_KILL_SESSION     = config.CMD_SEP.join(['tmux','kill-session', '-t%s'])
#capture pane content and save in given file. The first %s is the ANSI-ESC flag (-e); the second %s is paneIdstr
CMD_CAPTURE_PANE     = config.CMD_SEP.join(['tmux','capture-pane','-%sp', '-S-100000', '-t%s'])
CMD_SHOW_OPTION      = config.CMD_SEP.join(['tmux','show-options','-gv','%s'])
CMD_HAS_SESSION      = config.CMD_SEP.join(['tmux','has-session','-t%s'])
CMD_SET_PANE_PATH    = config.CMD_SEP.join(['tmux','send-keys','-t%s','cd \"%s\"\nclear\n'])
CMD_CLEAR_PANE       = config.CMD_SEP.join(['tmux','clear-history', '-t%s'])
CMD_LIST_WINDOWS     = config.CMD_SEP.join(['tmux','list-windows','-F#{window_index}:=:#{window_name}:=:#{window_active}:=:#{window_layout}','-t%s'])
CMD_MOVE_WINDOW      = config.CMD_SEP.join(['tmux','move-window','-s%s','-t%s'])
CMD_RENAME_WINDOW    = config.CMD_SEP.join(['tmux','rename-window','-t%s:%d','%s'])
CMD_NEW_EMPTY_WINDOW = config.CMD_SEP.join(['tmux','new-window','-d','-t%s:%d'])
CMD_ACTIVE_WINDOW    = config.CMD_SEP.join(['tmux','select-window','-t%s:%d'])
CMD_SPLIT_WINDOW     = config.CMD_SEP.join(['tmux','split-window','-d','-l3','-t%s:%d.%d'])
CMD_SET_LAYOUT       = config.CMD_SEP.join(['tmux','select-layout','-t%s:%d','%s'])
CMD_LOAD_CONTENT     = config.CMD_SEP.join(['tmux','send-keys','-t%s','cat   %s\n'])

def has_tmux_server():
    """check if there is a running tmux server"""
    cmd  = CMD_LIST_SESSIONS.split(config.CMD_SEP)
    code = util.cmd_return_code(cmd)
    return code == 0

def get_sessions():
    """ 
    return a list of tmux session names:size:attached
    like: sessName:=:(200,300):=:1
    """
    cmd = CMD_LIST_SESSIONS.split(config.CMD_SEP)
    s = util.exec_cmd(cmd)
    return s.split('\n')

def get_windows_from_session(sess_name):
    """
    return a list of windows by given tmux session name
    like: 1:=:W-name:=:1
    idx:=:name:=:active
    """
    cmd = (CMD_LIST_WINDOWS % sess_name).split(config.CMD_SEP)
    s = util.exec_cmd(cmd)
    return s.split('\n')
    
def get_panes_from_sess_win(sess_name,win_idx):
    """return list of result string
      output format: paneIdx:=:(width,height):=:path:=:active
    """
    p = (sess_name,win_idx)
    cmd = (CMD_LIST_PANES % p).split(config.CMD_SEP)
    s = util.exec_cmd(cmd)
    return s.split('\n')

def set_pane_path(pane_idstr, path):
    """ set pane path by 'send-key' and clear the screen"""
    cmd = (CMD_SET_PANE_PATH % (pane_idstr,path)).split(config.CMD_SEP)
    util.exec_cmd(cmd)
    #clear history
    cmd = (CMD_CLEAR_PANE%(pane_idstr)).split(config.CMD_SEP)
    util.exec_cmd(cmd)


def capture_pane(pane_idstr,filename):
    """
    capture pane content and save in given filename.
    the format of pane_idstr is: sessionName:winIdx.paneIdx
    """
    #read the config to decide if backup the ansi escapes
    p = ('e' if config.CNT_WITH_ESC else '', pane_idstr)
    cmd = (CMD_CAPTURE_PANE % p).split(config.CMD_SEP)
    util.exec_cmd_redir(cmd, filename)

def create_session(sess_name,size):
    p = (sess_name,size[0],size[1])
    cmd = (CMD_CREATE_SESSION % p).split(config.CMD_SEP)
    s = util.exec_cmd(cmd)

def create_empty_window(sess_name, base_index):
    p = (sess_name, int(base_index))
    cmd = (CMD_NEW_EMPTY_WINDOW % p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def split_window(sess_name, win_id, pane_min_id):
    p = (sess_name,int(win_id), int(pane_min_id))
    cmd = (CMD_SPLIT_WINDOW % p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def active_window(sess_name, win_id):
    p = (sess_name,win_id)
    cmd = (CMD_ACTIVE_WINDOW% p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def select_layout(sess_name, win_id, layout):
    p = (sess_name,win_id,layout)
    cmd = (CMD_SET_LAYOUT% p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def rename_window(sess_name, win_id, name):
    """
    rename the window in session
    """
    p = (sess_name, win_id, name)
    cmd = (CMD_RENAME_WINDOW % p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def renumber_window(sess_name, win_id_from, win_id_to):
    """
    renumber the window in session
    """
    p = (sess_name  + ':' + str(win_id_from), \
        sess_name + ':' + str(win_id_to))

    cmd = (CMD_MOVE_WINDOW % p).split(config.CMD_SEP)
    util.exec_cmd(cmd)

def get_option(option):
    """ get global option value """
    cmd = (CMD_SHOW_OPTION % option).split(config.CMD_SEP)
    return  util.exec_cmd(cmd)
    
def has_session(sess_name):
    """check if a session exists already"""
    cmd = (CMD_HAS_SESSION%sess_name).split(config.CMD_SEP)
    return util.cmd_return_code(cmd) == 0

def kill_session(sess_name):
    """kill a session, used for deleting dummy session"""
    cmd = (CMD_KILL_SESSION%sess_name).split(config.CMD_SEP)
    return util.cmd_return_code(cmd) == 0

def restore_pane_content(pane_idstr,filename):
    """restore backuped pane content.  """
    #put filename in quote, in case there is space, tab etc.
    filename = '"' + filename + '"'
    cmd = (CMD_LOAD_CONTENT %  (pane_idstr,filename)).split(config.CMD_SEP)
    util.exec_cmd(cmd)
