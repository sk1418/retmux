# -*- coding:utf-8 -*-
import subprocess
import re
import json
import os

def exec_cmd(cmd):
    """execute a shell command
    return the output with the last linebreak '\n' removed"""
    s = subprocess.check_output(cmd)
    if s:
        s = re.sub('\n$','',s)
    return s

def to_json(obj, parent_dir, filename):
    #if parent path doesn't exist, create the dir
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    jsonfile = os.path.join(parent_dir,filename)
    if obj:
        with open(jsonfile,'w') as f:
            json.dump(obj, f, default = lambda o: o.__dict__, sort_keys=True, indent=4)
