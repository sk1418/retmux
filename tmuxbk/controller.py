# -*- coding:utf-8 -*-
import util
import backup
import restore
import tmux_obj
import config
import datetime,time
import logging, log
import os,sys
from os import path 

LOG = log.get_logger()


tmux_dict = {}

def list_all_sessions():
    """print a list of all backuped sessions (with short info)"""
    if not len(tmux_dict.keys()):
        #name is empty, show all list(short info)
        l = util.all_backups()
        if not l or len(l) == 0:
            LOG.info("No backup was created yet.\nretmux -b [name] to create backup" )
            sys.exit()

        last = util.latest_backup().split('/')[-1]
        latest_tmux = util.get_tmux_by_id(last)
        #add into dict
        i=1
        tmux_dict[str(i)]=latest_tmux

        bk_list = [ b for b in l if b != last]
        for tmux_id in bk_list:
            tmux = util.get_tmux_by_id(tmux_id)
            i+=1
            tmux_dict[str(i)]=tmux

    list_fmt = '%s%2s %s'#fmt for list all, the first %s is the '*' place
    print util.get_line('=')
    #header
    print  list_fmt %(' ', 'No.',tmux_obj.Tmux.short_format%('Name','Sessions','Created on'))
    print util.get_line('=')
    keys = tmux_dict.keys()
    keys.sort()
    for idx in keys:
        tmux = tmux_dict[idx]
        latest_flag = '*' if idx == '1' else ' '
        print list_fmt%(latest_flag, idx, tmux.short_info())
    print util.get_line('-')
    print '%72s'%'Latest default backup with (*)'
        

def show_and_action(name=None, action=None):
    """list backups info. if name was given, show detailed info for given
        backup item. otherwise show short_info for all backups as list
        if there is action, will do the action after the details was displayed.
        the action should be a function with single argument of tmux_obj.Tmux instance
        """

    #using restore check function to validate the given name
    name = tmux_id_4_show(name)
    
    if not name:
        #interactively show details
        while 1:
            list_all_sessions()
            idx = raw_input("retmux> Please give backup No. (press q to exit):")

            if not idx:
                log.print_err("Invalid index: (empty)")
            elif idx.lower() == 'q':
                break
            elif not tmux_dict.has_key(idx):
               log.print_err("Invalid index: " + idx)
            else:
                tmux = tmux_dict[idx]
                print util.get_line('>')
                print log.hl('Details of backup:','bold') +'%s'% tmux.tid
                print util.get_line('>')
                print '\n'.join(tmux.long_info())
                print util.get_line('<')
                if action:
                    action(tmux)
    else:
        #till here, the name should be validated, exists
        print log.hl('Details of backup:','bold') +'%s'% name
        print util.get_line('=')
        tmux = util.get_tmux_by_id(name)
        print '\n'.join(tmux.long_info()) 
        if action:
            action(tmux)

def do_delete(name=None):
    """delete backup with given name
    if the given tmux_id is not empty, use it as backup name, otherwise
    delete delete interactively
    """
    show_and_action(name, action_delete)
     
def action_delete(tmux):
    if tmux and  isinstance(tmux, tmux_obj.Tmux):
        confirm = raw_input("retmux> " + log.hl('Delete','red') + " backup "+tmux.tid+"? [yes|no] ")
        if confirm.lower() == "yes":
            if util.delete_backup(tmux.tid) == 0:
                global tmux_dict
                tmux_dict={} #empty the dict
                LOG.info('Backup %s was deleted'%tmux.tid)
        
def do_backup(name=None):
    """backup current tmux sessions with given name
    if the given tmux_id is not empty, use it as backup name, otherwise
    use default timestamp string for name
    """
    name = tmux_id_4_backup(name)
    LOG.debug('backup name:%s'%name)
    backup.backup_tmux(name)

    
def do_restore(name=None):
    """restore sessions from named backup"""
    name = tmux_id_4_restore(name)
    restore.restore_tmux(name)

def interactive_restore():
    """restore sessions interactively"""
    show_and_action(None,action_restore)

def action_restore(tmux):
    if tmux and  isinstance(tmux, tmux_obj.Tmux):
        confirm = raw_input("retumx> restore "+tmux.tid+"? [yes|no] ")
        if confirm.lower() == "yes":
            do_restore(tmux.tid)
            LOG.info('Backup %s was restored' %tmux.tid)
            sys.exit()



def tmux_id_4_backup(tmux_id):
    """validate the given tmux_id, and return the valid value"""
    if not tmux_id:
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    if path.isdir(path.join(config.BACKUP_PATH,tmux_id)):
        LOG.error('(backup -b):the given backup name exists already, aborted.')
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
        LOG.error('(retore -r): backup dir is empty, nothing to restore')
        sys.exit(1)

    #checking tmux_id
    if tmux_id:
        if tmux_id not in all_bk:
            LOG.error('(restore -r): cannot find given backup name:%s'% tmux_id)
            sys.exit(1)
    else:
        tmux_id = util.latest_backup().split('/')[-1]
        print 'backup name is empty, using last backup:%s'%tmux_id

    return tmux_id

def tmux_id_4_show(tmux_id):
    """check the tmux_id (backup name) for show info (-l)
    """
    #if no backup exists, exit application
    all_bk =util.all_backups() 

    #checking tmux_id
    if tmux_id:
        if tmux_id not in all_bk:
            LOG.error('cannot find given backup name:%s'% tmux_id)
            sys.exit(1)

    return tmux_id

