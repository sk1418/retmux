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
    output = tmux_cmd.get_session_names()
    sess = []

    sesssion = None 
    for s in output:
        #s is like  sessName:[200,300]:1
        s_list = s.split(':')
        session =tmux_obj.Session(s_list[0]) 
        session.size = eval(s_list[1])
        session.attached = int(s_list[2])>0
        sess.append(session)
    return sess

if __name__ == '__main__':
    current_tmux()
