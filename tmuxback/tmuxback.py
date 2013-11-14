# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import datetime,time



def current_tmux():
    """get current tmux information and return Tmux object"""
    #id is timestamp
    id = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    tmux = tmux_obj.Tmux(id)
    tmux.sessions = load_sessions()
    util.to_json(tmux)


def load_sessions():
    """load sessions information """
    names = tmux_cmd.get_session_names()
    sess = []
    for n in names:
        sess.append(tmux_obj.Session(n))
    return sess

if __name__ == '__main__':
    current_tmux()
