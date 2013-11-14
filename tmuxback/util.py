# -*- coding:utf-8 -*-
import subprocess
import re
import json

def exec_cmd(cmd):
    """execute a shell command
    return the output with the last linebreak '\n' removed"""
    s = subprocess.check_output(cmd)
    if s:
        s = re.sub('\n$','',s)
    return s

def to_json(obj):
    if obj:
        with open("/tmp/test/x.json",'w') as f:
            json.dump(obj, f, default = lambda o: o.__dict__, sort_keys=True, indent=4)
