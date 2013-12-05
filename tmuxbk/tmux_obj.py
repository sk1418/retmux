# -*- coding:utf-8 -*-
from operator import attrgetter

class Tmux(object):
    """ a backuped Tmux object """
    def __init__(self, tid):
        self.tid = tid
        self.sessions = []
        self.create_time = ''

    def short_info(self):
        """ short info of this tmux object"""
        #TODO format the string.
        info = '%s %d sessions %s -backuped on %s'
        p = (self.tid, 
               len(self.sessions),
               [s.name for s in self.sessions],
               self.create_time)
        return info % p

    def long_info(self):
        """ longer info of this tmux object"""
        pass
class Session(object):
    def __init__(self,name):
        self.name = name
        self.attached = False
        self.size = ()
        self.windows = []

    def windows_in_reverse(self):
        """ 
        return the list of windows,
        but sorted by win_id descending
        """
        return sorted(self.windows, key=attrgetter('win_id'), reverse=True)

class Window(object):
    def __init__(self,sess_name,wid):
        #sessionName.windowIdx as id
        self.win_id = wid
        self.name = 'win' + str(wid)
        self.panes = []
        self.active= False
        self.sess_name = sess_name
        self.layout=''
        self.__min_pane_id = None

    def min_pane_id(self):
        if self.__min_pane_id == None :
            self.__min_pane_id = \
                    sorted(self.panes, key=attrgetter('pane_id'))[0] .pane_id
        return self.__min_pane_id


class Pane(object):
    """tmux pane object"""
    def __init__(self,sess_name,win_id,index):
        #string sessionName.windowIdx.paneIdx as id
        self.pane_id  = index
        self.size = ()
        self.path = '~'
        self.active= False
        self.sess_name = sess_name
        self.win_id = win_id
        self.cont_file=''

    def idstr(self):
        return self.sess_name+':'+str(self.win_id)+'.'+str(self.pane_id)
        
