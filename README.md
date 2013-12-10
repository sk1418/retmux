**retmux** README file

				  __
	   ________  / /_____ ___  __  ___  __
	  / ___/ _ \/ __/ __ `__ \/ / / / |/_/
	 / /  /  __/ /_/ / / / / / /_/ />  <  
	/_/   \___/\__/_/ /_/ /_/\__,_/_/|_|

				- a tmux backup/reload tool

##Introduction

##Features

- configurable options for (logging, ANSI escapes)
- (non- or) interactive operations (list/delete/restore) backups
- highlighted output
- most important: tmux sessions backup and restore :) 

###What can be backuped/restored?
- **sessions** : with names
- **windows** : with name, order, pane split and split layout
- **panes**  : with path and content with same look and feel (ANSI escapes)

###What can NOT be backuped/restored?
- the processes/programs running in window or pane at backup time
- command history in each window






- 

##Installation

- tbd

##Usage

    [USAGE] 
        retmux [OPTIONS] 
    [OPTIONS] 
        -h print help message

        -v version

        -l [name] : list backup info
               with [name]: show detailed backup info by name
            without [name]: show brief and detailed info interactively

        -d [name] : delete a backup
               with [name]: delete by given name
            without [name]: delete interactively

        -b [name] : backup current tmux sessions
               with [name]: name the backup with given name
            without [name]: name the backup with default name(timestamp)

        -r [name] : restore tmux sessions from backup
               with [name]: restore sessions by backup name
            without [name]: restore from the latest backup

        -ri       : restore sessions interactively

##Screenshots
tbd
