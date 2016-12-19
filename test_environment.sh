#!/bin/bash

#---------------------------------------------
#              COLORS
#---------------------------------------------

export RED='\033[0;31m'
export GREEN='\033[0;32m'
export LGREEN='\033[1;32m'
export YELLOW='\033[1;33m'
export NC='\033[0m' # No Color


# -------------------------------------------
# color_prefix(): arg1 - color, arg2 - msg
color_prefix() {
	eval "local COLOR=\$$1"
	echo -e "${COLOR}***${NC}$2"
}

export -f color_prefix

