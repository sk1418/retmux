# -*- coding:utf-8 -*-

class Tmux(object):
    def __init__(self, id):
        self.id = id
        self.sessions = []

class Session(object):
    def __init__(self,name):
        self.name = name
        self.attached = False
        self.size = ()
        self.windows = []

class Window(object):
    def __init__(self,sess_name,id):
        #sessionName.windowIdx as id
        self.id=id
        self.name = 'win' + str(id)
        self.panes = []
        self.active= False
        self.sess_name = ''

class Pane(object):
    """tmux pane object"""
    def __init__(self,sess_name,win_id,id):
        #string sessionName.windowIdx.paneIdx as id
        self.id=id
        self.size = ()
        self.path = '~'
        self.active= False
        self.sess_name = sess_name
        self.win_id = win_id
        
