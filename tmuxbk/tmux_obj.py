# -*- coding:utf-8 -*-
from operator import attrgetter
import log

LOG = log.get_logger()

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
        sess_fmt   = u'─Session─┬─[%s] (%d windows):'
        win_fmt    = u'─Window─┬─(%d) [%s] (%d panes):'
        pane_fmt   = u'─' + log.hl('Pane','green') +' (%d) %s'
        info.append("%72s" % ('Backup was created on ' + self.create_time))

        info.append(backup_fmt %(log.hl(self.tid,'bold'), len(self.sessions)))
        
        last_s = self.sessions[-1]
        for s in self.sessions:
            is_last_s = s.name == last_s.name
            s_info = sess_fmt % ( log.hl(s.name,'cyan'), len(s.windows))
            info.append( tree_struc(s_info, [is_last_s],lvl=1))
            last_w = s.windows[-1]
            for w in s.windows:
                is_last_w = w.win_id == last_w.win_id
                w_info = win_fmt % (w.win_id, log.hl(w.name,'blue'), len(w.panes))
                info.append(tree_struc(w_info, [is_last_s,is_last_w],lvl=2))
                last_p = w.panes[-1]
                for p in w.panes:
                    p_info = pane_fmt%( p.pane_id, p.path)
                    is_last_p = last_p.pane_id == p.pane_id
                    info.append(tree_struc(p_info, [is_last_s,is_last_w,is_last_p],lvl=3))
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
        

#constants for the node tree
PIPE        = u'│'
NORMAL_NODE = u'├'
LAST_NODE   = u'└'

SPACE       = u' '*8

def tree_struc(text,islast_list,lvl,place_holder=False):
    """
    recursively build the tree structure for tmux objects.
    
    para:
    text : the object info text
    islast_list: a list of boolean, if the node is last node on each level 
    lvl: level
    place_holder: default False. The current node would be handled as place holder or normal node line.
    """
    if lvl > 0:
        lvl -= 1
        if islast_list[lvl]:
            text = SPACE + (' ' if place_holder else LAST_NODE )+  text
        else:
            text = SPACE + (PIPE if place_holder else NORMAL_NODE )+ text
        #here add one space for alignment. because len('session')-len('window')=1
        if lvl ==1 :
            text =' ' +  text 
        return tree_struc(text,islast_list,lvl,True)
    return  text
    

