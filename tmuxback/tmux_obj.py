# -*- coding:utf-8 -*-

class Tmux(object):
    def __init__(self, id):
        self.id = id
        self.sessions = []

class Session(object):
    def __init__(self,name):
        self.name = name
        self.attached = False
        self.size = []
        self.windows = []

class Window(object):
    def __init__(self, name):
        #sessionName.windowIdx as id
        self.id=''
        self.name = name
        self.panels = []
        self.index = 0
        self.active= 0

class Pane(object):
    """tmux pane object"""
    def __init__(self):
        #string sessionName.windowIdx.paneIdx as id
        self.id=''
        self.index = 0
        self.size = []
        pass
