# -*- coding:utf-8 -*-
import util
import tmux_cmd
import tmux_obj
import config
import datetime,time
import os
from os import path 



def restore_tmux(tmux_id):
    """
    retore tmux sessions by given backuped Tmux id
    0 - read all backups from $HOME/.tmuxback/backup
    1 - if the given tmux_id is empty, take the latest
    2 - throw error msg if given name doesn't exist
    3 - check if there is tmux running and with same session name
    4 - handle windows, panes ..
    """

    pass


if __name__ == '__main__':
    restore_tmux()
