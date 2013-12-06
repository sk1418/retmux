from os import path 
import os
import shutil, sys
import ConfigParser


VERSION     = '1.0.0'                #software version
#the separator of tmux command output
SEP         = ':=:'
APP_PATH    = path.join(path.dirname(__file__),"../")
USER_PATH   = path.join(os.getenv("HOME") , ".tmuxback")
SAMPLE_CONF = path.join(APP_PATH, 'sample','default.conf')
BACKUP_PATH = path.join(USER_PATH, "backup")
CONF_FILE   = path.join(USER_PATH, "tmuxback.conf")

def update_config(section, key, value):
    """ update the given config option"""
    cf = ConfigParser.ConfigParser()
    with open( CONF_FILE, 'r') as cfgf:
        cf.readfp(cfgf)
    cf.set(section, key, value)
    with open(CONF_FILE, 'w') as cfgf:
        cf.write(cfgf)



def load_config():
    """
        load config from config file 
        return True if sucessful, otherwise False
    """
    cf = ConfigParser.ConfigParser()
    
    # if conf file doesn't exist, cp default conf there
    if not path.exists(CONF_FILE):
        __init_config()

    cf.read(CONF_FILE);

    #load options here
    #TODO
    return True;

def __init_config():
    """
    create .tmuxback under home
    """
    #mkdir and copy files
    os.makedirs(BACKUP_PATH)
    shutil.copy(SAMPLE_CONF,USER_PATH)
