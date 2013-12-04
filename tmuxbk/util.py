# -*- coding:utf-8 -*-
import subprocess
import re
import json
import os
import config
import logging
import tmux_obj

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
            json.dump(obj, f, default = tmux_obj.object2dict, sort_keys=True, indent=4)

def json_to_obj(jsonfile):
    """load json file
    the file would be the absolute path of json
    """

    tmux = None
    with open(jsonfile,'r') as f:
        tmux = json.load(f, object_hook=tmux_obj.dict2object)
    return tmux


def all_backups():
    """get all saved tmux backups"""
    bkdir = config.BACKUP_PATH
    return [d for d in os.listdir(bkdir) if os.path.isdir(os.path.join(bkdir,d))]

def latest_backup():
    """get latest backup"""
    return max([os.path.join(config.BACKUP_PATH,p) for p in all_backups()], key=os.path.getmtime)

def setup_log(console_lvl, file_lvl):
    """setup_log, this function should be called only once at the beginning of application starts"""
    logger = logging.getLogger('tmuxbackLogger')
    logger.setLevel(file_lvl)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(config.USER_PATH,'tmuxback.log'))
    fh.setLevel(file_lvl)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(console_lvl)

    # create formatter and add it to the handlers
    fhFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    chFormatter = logging.Formatter('%(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s') \
            if console_lvl == logging.DEBUG else logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh.setFormatter(fhFormatter)
    ch.setFormatter(chFormatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    logger.info("Log system setup successfully")

def get_logger():
    return logging.getLogger('tmuxbackLogger')
