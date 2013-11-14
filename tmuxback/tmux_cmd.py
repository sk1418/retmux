# -*- coding:utf-8 -*-
import subprocess
import re
import util


#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S'
CMD_LIST_WINDOWS='tmux list-windows -F#{window_index}:#{window_name} -t%s'



def get_session_names():
    """ return a list of tmux session names """
    cmd = CMD_LIST_SESSIONS.split(' ')
    s = util.exec_cmd(cmd)
    return s.split('\n')

def get_windows_from_session(session):
    """return a dict {index:win_name} of windows by given session"""
    cmd = (CMD_LIST_WINDOWS % session).split(' ')
    s = util.exec_cmd(cmd)
    l = s.split('\n')
    return dict(x.split(':') for x in l)
    






if __name__ == '__main__':
    print get_windows_from_session('TEST2')
