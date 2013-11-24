# -*- coding:utf-8 -*-
import subprocess
import re
import json
import os
import config

def exec_cmd(cmd):
    """execute a shell command
    return the output with the last linebreak '\n' removed"""
    s = subprocess.check_output(cmd)
    if s:
        s = re.sub('\n$','',s)
    return s

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
            json.dump(obj, f, default = lambda o: o.__dict__, sort_keys=True, indent=4)

def all_backups():
    """get all saved tmux backups"""
    return [d for d in os.listdir(config.BACKUP_PATH) if os.path.isdir(d)]

def latest_backup():
    """get latest backup"""
    return max(all_backups(), key=os.path.getmtime())
