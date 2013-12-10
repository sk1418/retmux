# -*- coding:utf-8 -*-
import subprocess
import re
import json
import os
import config
import tmux_obj
import shutil
import random, string


def object2dict(obj):
    """convert object to a dict"""
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

        for subm in module_name.split('.')[1:]:
            module = getattr(module, subm)
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

def get_tmux_by_id(tmux_id):
    """get tmux object by given tmux_id
    this will build json and deserializing
    """
    jsonfile = os.path.join(config.BACKUP_PATH,tmux_id,tmux_id+'.json')
    return json_to_obj(jsonfile)

def delete_backup(tmux_id):
    """delete backup by tmux_id (backup name) """
    tmux_dir = os.path.join(config.BACKUP_PATH, tmux_id)
    try:
        shutil.rmtree(tmux_dir)
        return 0
    except:
        return 1


def exec_cmd(cmd):
    """execute a shell command
    the cmd argument is a list
    return the output with the last linebreak '\n' removed"""
    s = subprocess.check_output(cmd)
    if s:
        s = re.sub('\n$','',s)
    return s
def cmd_return_code(cmd):
    """execute a shell command
    the cmd argument is a list
    return the return code"""
    return subprocess.call(cmd)
    


def exec_cmd_redir(cmd, file_fullname):
    """execute a shell command
    redirect the output to the file"""
    with open(file_fullname, 'w') as fout:
        subprocess.call(cmd, stdout=fout)

def to_json(obj, parent_dir, filename):
    #if parent path doesn't exist, create the dir
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    jsonfile = os.path.join(parent_dir,filename)
    if obj:
        with open(jsonfile,'w') as f:
            json.dump(obj, f, default = object2dict, sort_keys=True, indent=4)

def json_to_obj(jsonfile):
    """load json file
    the file would be the absolute path of json
    """

    tmux = None
    with open(jsonfile,'r') as f:
        tmux = json.load(f, object_hook=dict2object)
    return tmux

def random_str(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def all_backups():
    """get all saved tmux backups"""
    bkdir = config.BACKUP_PATH
    return [d for d in os.listdir(bkdir) if os.path.isdir(os.path.join(bkdir,d))]
def latest_backup():
    """get latest backup"""
    return max([os.path.join(config.BACKUP_PATH,p) for p in all_backups()], key=os.path.getmtime)

def get_line(s):
    """get a gui line with given char"""
    return str(s)*72
