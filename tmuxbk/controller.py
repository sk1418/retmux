# -*- coding:utf-8 -*-
import util
import tmux_backup
import tmux_restore
import logging

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
    """backup current tmux sessions with given name"""
    pass
    
def restore(name=None):
    """restore sessions from named backup"""
    pass
