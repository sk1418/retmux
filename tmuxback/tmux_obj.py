# -*- coding:utf-8 -*-
from operator import attrgetter

class Tmux(object):
    def __init__(self, tid):
        self.tid = tid
        self.sessions = []
    

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
        self.sess_name = ''
        self.layout=''
        self.__min_pane_id = None

    def min_pane_id():
        if self.__min_pane_id == None :
            self.__min_pane_id = sorted(self.panes, key=attrgetter('pane_id'))[0] 
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
        

#-------------------------------------------------
# helper method for json and object instantiation
#-------------------------------------------------
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d

def dict2object(d):
    """ json decode function"""
    #convert dict to object
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)

        if class_name == 'Tmux':
            obj = class_(d['tid'])
        elif class_name == 'Window':
            obj = class_(d['sess_name'],d['win_id'])
        elif class_name == 'Session':
            obj = class_(d['name'])
        elif class_name == 'Pane':
            obj = class_(d['sess_name'],d['win_id'],d['pane_id'])

        for k, v in d.items():
            setattr(obj,k,v)
    else:
        obj = d
    return obj

