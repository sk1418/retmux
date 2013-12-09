# -*- coding:utf-8 -*-
from operator import attrgetter

class Tmux(object):
    short_format = '%-17s %-30s %s'
    """ a backuped Tmux object """
    def __init__(self, tid):
        self.tid = tid
        self.sessions = []
        self.create_time = ''

    def short_info(self):
        """ short info of this tmux object"""
        p = (self.tid, 
             ', '.join([s.name for s in self.sessions]),
             self.create_time)
        return Tmux.short_format % p

    def long_info(self):
        """ longer info of this tmux object"""
        info = []

        backup_fmt = u' Backup─┬─[%s] (%d sessions):'
        sess_fmt   = u'%s─Session─┬─[%s] (%d windows):'
        win_fmt    = u'%s─Window─┬─(%d) [%s] (%d panes):'
        pane_fmt   = u'%s─Pane─(%d) %s'
        info.append("%72s" % ('Backup was created on ' + self.create_time))

        info.append(backup_fmt %(self.tid, len(self.sessions)))
        
        last_s = self.sessions[-1]
        for s in self.sessions:
            is_last_s = s.name == last_s.name
            info.append(sess_fmt % (tree_str(s,is_last_s,False,False),
                                    s.name, 
                                    len(s.windows)))
            last_w = s.windows[-1]
            for w in s.windows:
                is_last_w = w.win_id == last_w.win_id
                info.append( win_fmt % (tree_str(w, is_last_s, is_last_w, False),
                                        w.win_id, w.name, 
                                        len(w.panes)))
                last_p = w.panes[-1]
                for p in w.panes:
                    is_last_p = last_p.pane_id == p.pane_id
                    info.append( pane_fmt%(tree_str(p,is_last_s, is_last_w, is_last_p),
                                            p.pane_id,
                                            p.path))

        return info


        

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
        
def tree_str(node,last_session,last_win,last_pane):
    """build the tree structure lines"""
    space = ' '*8
    result = space

    pipe = u'│'

    #normal char
    nch = u'├'

    #last char
    lch   = u'└'


    if isinstance(node,Session):
        result += lch if last_session else nch
    elif isinstance(node, Window):
        result += ' ' if last_session else pipe
        result += space + ' ' # because len('session')-len('window')=1
        result += lch if last_win else nch
    elif isinstance(node, Pane):
        result += ' ' if last_session else pipe
        result += space + ' ' # because len('session')-len('window')=1
        result += ' ' if last_win else pipe
        result += space
        result += lch if last_pane else nch

    return result
