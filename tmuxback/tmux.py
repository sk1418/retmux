# -*- coding:utf-8 -*-
import subprocess
import re


#tmux commands

#list sessions
CMD_LIST_SESSIONS='tmux list-sessions -F#S'



def get_session_names():
    """ return a list of tmux session names """
    s = subprocess.check_output(CMD_LIST_SESSIONS.split(' '))
    s = re.sub('\n$','',s)
    return s.split('\n')

#if __name__ == '__main__':
#    print get_session_names()
