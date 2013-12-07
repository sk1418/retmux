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

#TODO refactory, move interactive part to a module?
#extract the list all and print part to a function.
def show_info(name=None):
    """list backups info. if name was given, show detailed info for given
        backup item. otherwise show short_info for all backups as list"""

    #using restore check function to validate the given name
    name = tmux_id_4_show(name)
    
    if not name:
        #name is empty, show all list(short info)
        l = util.all_backups()
        if not l or len(l) == 0:
            LOG.info( "No backup was created yet.\ntmuxback -b [name] to create backup" )
        else:
            list_fmt = '%s%2s %s'#fmt for list all, the first %s is the '*' place
            tmux_dict = {}
            i = 0

            LOG.info(util.get_line('='))
            LOG.info( list_fmt %(' ', 'Id',tmux_obj.Tmux.short_format%('Name','Sessions','Create on')))
            LOG.info(util.get_line('='))
            last = util.latest_backup().split('/')[-1]
            latest_tmux = util.get_tmux_by_id(last)
            #add into dict
            i+=1
            tmux_dict[str(i)]=latest_tmux

            bk_list = [ b for b in l if b != last]

            LOG.info(list_fmt%('*',str(i),latest_tmux.short_info()))

            for tmux_id in bk_list:
                tmux = util.get_tmux_by_id(tmux_id)
                i+=1
                tmux_dict[str(i)]=tmux
                LOG.info(list_fmt%(' ',str(i),tmux.short_info()))
            LOG.info(util.get_line('-'))
            LOG.info('%72s'%'Latest default backup with (*)')
            #interactively show details
            while 1:
                idx = raw_input("tmuxback> Show details of Id (press q to exit):")

                if not idx:
                    LOG.error("invalid index: (empty)")
                elif idx.lower() == 'q':
                    break
                elif not tmux_dict.has_key(idx):
                    LOG.error("invalid index:" + idx)
                else:
                    tmux = tmux_dict[idx]
                    LOG.info('\nDetails of backup:%s'% tmux.tid)
                    LOG.info(util.get_line('-'))
                    LOG.info('\n'.join(tmux.long_info()))
                    break

    else:
        #till here, the name should be validated, exists
        LOG.info('\nDetails of backup:%s'% name)
        LOG.info(util.get_line('='))
        tmux = util.get_tmux_by_id(name)
        LOG.info('\n'.join(tmux.long_info()))
       
def backup(name=None):
    """backup current tmux sessions with given name
    if the given tmux_id is not empty, use it as backup name, otherwise
    use default timestamp string for name
    """
    name = tmux_id_4_backup(name)
    LOG.debug('backup name:%s'%name)
    backup.backup_tmux(name)

    
def restore(name=None):
    """restore sessions from named backup"""
    name = tmux_id_4_restore(name)
    restore.restore_tmux(name)


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

def tmux_id_4_show(tmux_id):
    """check the tmux_id (backup name) for show info (-l)
    """
    #if no backup exists, exit application
    all_bk =util.all_backups() 

    #checking tmux_id
    if tmux_id:
        if not all_bk.__contains__(tmux_id):
            LOG.error('cannot find given backup name:%s'% tmux_id)
            sys.exit(1)

    return tmux_id

