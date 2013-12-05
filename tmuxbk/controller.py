# -*- coding:utf-8 -*-
import util
import tmux_backup
import tmux_restore
import config
import datetime,time
import logging
import os,sys
from os import path 

LOG = util.get_logger()

def list_all():
    """list all backups"""
#TODO the current impl. is rather simple, just list the backup names. 
#     It would be nice to list backups with some tmux session info.
#     tmux object might need to be changed by adding some fields
#     backup/writing to json module needs to be changed too.
    l = util.all_backups()
    if not l or len(l) == 0:
        print "No backup was created yet.\ntmuxback -b [name] to create backup" 
    else:
        last = util.latest_backup().split('/')[-1]
        l = [ b for b in l if b != last]
        print "Tmux backups list:(the latest default backup name with '*'):"
        print "(*)"+last
        print '\n'.join(l)
       
def backup(name=None):
    """backup current tmux sessions with given name
    if the given tmux_id is not empty, use it as backup name, otherwise
    use default timestamp string for name
    """
    name = tmux_id_4_backup(name)
    LOG.debug('backup name:%s'%name)
    tmux_backup.backup_tmux(name)

    
def restore(name=None):
    """restore sessions from named backup"""
    name = tmux_id_4_restore(name)
    tmux_restore.restore_tmux(name)


def tmux_id_4_backup(tmux_id):
    """validate the given tmux_id, and return the valid value"""
    if not tmux_id:
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    if path.isdir(path.join(config.BACKUP_PATH,tmux_id)):
        LOG.error('the given backup name exists already, aborted.')
        sys.exit(1)
    return tmux_id


def tmux_id_4_restore(tmux_id):
    """check the tmux_id (backup name) for restore
    0 - read all backups from $HOME/.tmuxback/backup
    1 - if the given tmux_id is empty, take the latest
    2 - throw error msg if given name doesn't exist
    """
    #if no backup exists, exit application
    all_bk =util.all_backups() 
    if len(all_bk)<1:
        LOG.error('backup dir is empty, nothing to restore')
        sys.exit(1)

    #checking tmux_id
    if tmux_id:
        if not all_bk.__contains__(tmux_id):
            LOG.error('cannot find given backup name:%s'% tmux_id)
            sys.exit(1)
    else:
        tmux_id = util.latest_backup().split('/')[-1]
        LOG.info('backup name is empty, using last backup:%s'%tmux_id)

    return tmux_id
