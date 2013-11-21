# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import datetime,time

#the separator of tmux command output
SEP=':=:'

def current_tmux():
    """get current tmux information and return Tmux object"""
    #id is timestamp
    id = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    tmux = tmux_obj.Tmux(id)
    tmux.sessions = load_sessions()
    util.to_json(tmux)


def load_sessions():
    """load sessions information """
    output = tmux_cmd.get_sessions()
    sess = []

    for s in output:
        #s is like  sessName:[200,300]:1
        s_l = s.split(SEP)
        session =tmux_obj.Session(s_l[0]) 
        session.size = eval(s_l[1])
        session.attached = int(s_l[2])>0
        #load windows
        session.windows = load_windows(session.name)
        sess.append(session)
    return sess

def load_windows(s_name):
    """load windows for given session name"""
    output = tmux_cmd.get_windows_from_session(s_name)
    wins = []
    for s in output:
        #s is like 1:wname:1
        w_l = s.split(SEP)
        win = tmux_obj.Window(int(w_l[0]))
        win.name = w_l[1]
        win.active = int(w_l[2])
        wins.append(win)
    return wins
        




if __name__ == '__main__':
    current_tmux()
