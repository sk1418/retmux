from os import path 
import os
import shutil, sys
import ConfigParser

VERSION     = '1.0.0'                #software version
APP_PATH    = path.join(path.dirname(__file__),"../")
USER_PATH   = path.join(os.getenv("HOME") , ".tmuxback")
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

def init_needed():
    """
    check if the home config directory exists
    """
    return not path.exists(USER_PATH)

def loadConfig():
    """
        load config from config file 
        return True if sucessful, otherwise False
    """
    cf = ConfigParser.ConfigParser()
    
    # if conf file doesn't exist, return False
    if not path.exists(CONF_FILE):
        return False

    cf.read(CONF_FILE);

    #load options here
    #TODO
    return True;

