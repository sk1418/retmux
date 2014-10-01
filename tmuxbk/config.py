from os import path 
import os
import shutil, sys
import ConfigParser
import log


VERSION     = '1.0.1'                #software version
#shell command separator
CMD_SEP     = u'\x97'
#the separator of tmux command output
SEP         = ':=:'
PKG_PATH    = path.dirname(__file__)
APP_PATH    = path.join(PKG_PATH,"../")
USER_PATH   = path.join(os.getenv("HOME") , ".retmux")
SAMPLE_CONF = path.join(PKG_PATH, 'conf','default.conf')
BACKUP_PATH = path.join(USER_PATH, "backup")
CONF_FILE   = path.join(USER_PATH, "retmux.conf")

######user config####
WITH_CNT = None
CNT_WITH_ESC = True
LOG_LVL_FILE = 'INFO'
LOG_LVL_CONSOLE = 'INFO'


def load_config():
    global LOG_LVL_FILE, LOG_LVL_CONSOLE, CNT_WITH_ESC
    """
        load config from config file 
        return True if sucessful, otherwise False
    """
    cf = ConfigParser.ConfigParser()
    
    # if conf file doesn't exist, cp default conf there
    if not path.exists(CONF_FILE):
        init_config()

    cf.read(CONF_FILE);

    #load options here
    try:
        lvl_file = cf.get('settings','log.level.file')
        lvl_console = cf.get('settings','log.level.console')
        CNT_WITH_ESC = cf.getboolean('settings','content.with.escape')

        if lvl_file.lower() not in log.LVL_DICT.keys():
            log.print_warn("cannot load log.level.file config, use default: %s" % LOG_LVL_FILE)
        else:
            LOG_LVL_FILE = lvl_file

        if lvl_console.lower() not in log.LVL_DICT.keys():
            log.print_warn("cannot load log.level.console config, use default: %s" %LOG_LVL_CONSOLE)
        else:
            LOG_LVL_CONSOLE = lvl_console
    except:

        log.print_warn('Error occured when loading config, using all default values')
        return False
    return True;

def init_config():
    """
    create .retmux under home
    """
    #mkdir and copy files
    os.makedirs(BACKUP_PATH)
    shutil.copy(SAMPLE_CONF,CONF_FILE)
