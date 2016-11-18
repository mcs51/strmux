#!/bin/bash

#---------------------------------------------
#              COLORS
#---------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
LGREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


# -------------------------------------------
# color_prefix(): arg1 - color, arg2 - msg
color_prefix() {
	eval "local COLOR=\$$1"
	echo -e "${COLOR}***${NC}$2"
}

# --------------------------------------------
#              SETTINGS
# --------------------------------------------
error=1
warning=2
debug=3
info=4

LEVEL=$warning
SILENT=1
SYSVERBOSE=0
VERBOSE=0
LOG=/home/ekat/docs/studying/programming/bash/task_parser/log.txt
SYSLOG=/home/ekat/docs/studying/programming/bash/task_parser/syslog.txt

#-----------------------------------------
#           SEND FUNCTIONS
#-----------------------------------------

sendDISP() {
	color_prefix "LGREEN" "$1"
}
export -f sendDISP

sendINFO() { 
	color_prefix "LGREEN" "$1"
	if (( $LEVEL>=$info )); then echo "$1" >$LOG
	fi
}
export -f sendINFO

sendWARN() {
	if (( $SILENT != 0 )); then color_prefix "YELLOW" $1
	fi
	
	if (( $LEVEL >= $warning )); then echo "$1" >$LOG
	fi
}

sendERR(){
	color_prefix "RED" "$1" >&2
	if (( $LEVEL>=$warning )); then echo "$1" >$LOG
	fi
}

sendDBGLOG(){
	if (( $SYSVERBOSE == 0 )); then color_prefix "YELLOW" "$1" >&2
	fi
	
	if (( $LEVEL>=$debug )); then echo "$1" >$LOG
	fi
}

sendDBG(){
	if (( $VERBOSE == 0 )); then color_prefix "GREEN" "$1"
	fi
	
	if (( $LEVEL>=$debug )); then echo "$1" >$LOG
	fi
}

sendSYSWARN(){
	if (( $VERBOSE == 0 )); then color_prefix "YELLOW" "$1"
	fi
	
	if (( $LEVEL>=$warning )); then echo "$1" >$SYSLOG
	fi
}

sendSYSERR(){
	color_prefix "RED" $1 >&2
	
	if (( $LEVEL>=$error )); then echo "$1" >$SYSLOG
	fi
}

sendSYSDBG(){
	if (( $SYSVERBOSE == 0 )); then color_prefix "RED" "$1" >&2
	fi
	
	if (( $LEVEL>=$debug )); then echo "$1" >$SYSLOG
	fi
}

#-----------------------------------------
#                MAIN  
#-----------------------------------------


exec 100> >( while read line; do sendDISP "$line"; done )
#exec 101> >( while read line; do sendINFO "$line"; done )
#exec 102> >( while read line; do sendWARN "$line"; done )
#exec 103> >( while read line; do sendERR "$line"; done )
#exec 104> >( while read line; do sendDBGLOG "$line"; done )
#exec 105> >( while read line; do sendDBG "$line"; done )
#exec 106> >( while read line; do sendSYSWARN "$line"; done )
#exec 107> >( while read line; do sendSYSERR "$line"; done )
#exec 108> >( while read line; do sendSYSDBG "$line"; done )

/home/ekat/docs/studying/programming/C_language/a.out /home/ekat/docs/studying/programming/C_language/test.txt

sleep 0.1

