#!/bin/bash

_init() {
    ##
    ## Initialize the script variables depending of the environment
    ##

    export _ERROR=0

    case $TERM in
        xterm*|screen)
            export _DUMBTERM=0
            export LINES=$(stty size | cut -d ' ' -f 1)
            export COLUMNS=$(stty size | cut -d ' ' -f 2)
            export _COLOR_SUCCESS="\e[1;32m"
            export _COLOR_INFO="\e[1;37m"
            export _COLOR_ERROR="\e[1;31m"
            export _COLOR_WARNING="\e[1;33m"
            export _COLOR_BULLET="\e[1;34m"
            export _COLOR_TITLE="\e[1;36m"
            export _COLOR_NORMAL="\e[0m"
            ;;
        *)
            export _DUMBTERM=1
            export LINES=24
            export COLUMNS=80
            ;;
    esac
}

_exec() {
    ##
    ## Execute a command
    ##

    # Display the command
    if [ $_DUMBTERM == 0 ] ; then
        if [ $(echo -n "$*" | wc -c) -gt $(($COLUMNS - 12)) ] ; then
            msg=$(echo "$*" | head -c $(($COLUMNS - 15)))
            echo -en "  ${_COLOR_BULLET}>${_COLOR_NORMAL} ${msg}"
            echo -en "... "
        else
            echo -en "  ${_COLOR_BULLET}>${_COLOR_NORMAL} $*"
            echo -en "\e[$(($COLUMNS - $(echo -n "$*" | wc -c) - 11))C"
        fi
    else
        echo -n "  > $* "
    fi
    # Exec the command and display the result
    output=$("$@" 2>&1) \
        && (echo -e "${_COLOR_BULLET}[${_COLOR_SUCCESS} OK ${_COLOR_BULLET}]${_COLOR_NORMAL}") \
        || {
               echo -e "${_COLOR_BULLET}[${_COLOR_ERROR}FAIL${_COLOR_BULLET}]${_COLOR_NORMAL}";
               echo -e "\n${_COLOR_ERROR}--------------------";
               echo "$output";
               echo -e "--------------------${_COLOR_NORMAL}\n";
               export _ERROR=$(($_ERROR + 1));
           }
}

_title() {
    ##
    ## Write a title
    ##

    echo -e "\n${_COLOR_BULLET}::${_COLOR_TITLE} $*${_COLOR_NORMAL}\n"
}


_init
export RIVALCFG_DRY=true
python --version


_title "Rival Mouse"

export RIVALCFG_PROFILE=1038:1384

_exec python -m rivalcfg -h
_exec python -m rivalcfg -l

_exec python -m rivalcfg -c red
_exec python -m rivalcfg -c f00
_exec python -m rivalcfg -c FF0000
_exec python -m rivalcfg -c "#fF0000"

_exec python -m rivalcfg -e breath
_exec python -m rivalcfg -e steady
_exec python -m rivalcfg -e 1

_exec python -m rivalcfg -p 125
_exec python -m rivalcfg -p 1000

_exec python -m rivalcfg -s 50
_exec python -m rivalcfg -s 6500

_exec python -m rivalcfg -S 50
_exec python -m rivalcfg -S 6500

_exec python -m rivalcfg -C red
_exec python -m rivalcfg -C f00
_exec python -m rivalcfg -C FF0000
_exec python -m rivalcfg -C "#fF0000"

_exec python -m rivalcfg -E breath
_exec python -m rivalcfg -E steady
_exec python -m rivalcfg -E 1

_exec python -m rivalcfg -r


_title "Rival 100 Mouse"

export RIVALCFG_PROFILE=1038:1702

_exec python -m rivalcfg -h
_exec python -m rivalcfg -l

_exec python -m rivalcfg -b default
_exec python -m rivalcfg -b os

_exec python -m rivalcfg -c red
_exec python -m rivalcfg -c f00
_exec python -m rivalcfg -c FF0000
_exec python -m rivalcfg -c "#fF0000"

_exec python -m rivalcfg -e breath
_exec python -m rivalcfg -e steady
_exec python -m rivalcfg -e 1

_exec python -m rivalcfg -p 125
_exec python -m rivalcfg -p 1000

_exec python -m rivalcfg -s 250
_exec python -m rivalcfg -s 4000

_exec python -m rivalcfg -S 250
_exec python -m rivalcfg -S 4000

_exec python -m rivalcfg -r


_title "Rival 300 Mouse"

export RIVALCFG_PROFILE=1038:1710

_exec python -m rivalcfg -h
_exec python -m rivalcfg -l

_exec python -m rivalcfg -c red
_exec python -m rivalcfg -c f00
_exec python -m rivalcfg -c FF0000
_exec python -m rivalcfg -c "#fF0000"

_exec python -m rivalcfg -e breath
_exec python -m rivalcfg -e steady
_exec python -m rivalcfg -e 1

_exec python -m rivalcfg -p 125
_exec python -m rivalcfg -p 1000

_exec python -m rivalcfg -s 50
_exec python -m rivalcfg -s 6500

_exec python -m rivalcfg -S 50
_exec python -m rivalcfg -S 6500

_exec python -m rivalcfg -C red
_exec python -m rivalcfg -C f00
_exec python -m rivalcfg -C FF0000
_exec python -m rivalcfg -C "#fF0000"

_exec python -m rivalcfg -E breath
_exec python -m rivalcfg -E steady
_exec python -m rivalcfg -E 1

_exec python -m rivalcfg -r


_title "Rival 300 CS:GO Fade Edition Mouse"

export RIVALCFG_PROFILE=1038:1394

_exec python -m rivalcfg -h
_exec python -m rivalcfg -l

_exec python -m rivalcfg -b default
_exec python -m rivalcfg -b os

_exec python -m rivalcfg -c red
_exec python -m rivalcfg -c f00
_exec python -m rivalcfg -c FF0000
_exec python -m rivalcfg -c "#fF0000"

_exec python -m rivalcfg -e breathslow
_exec python -m rivalcfg -e breathmed
_exec python -m rivalcfg -e breathfast
_exec python -m rivalcfg -e steady
_exec python -m rivalcfg -e 4
_exec python -m rivalcfg -e 3
_exec python -m rivalcfg -e 2
_exec python -m rivalcfg -e 1

_exec python -m rivalcfg -E breathslow
_exec python -m rivalcfg -E breathmed
_exec python -m rivalcfg -E breathfast
_exec python -m rivalcfg -E steady
_exec python -m rivalcfg -E 4
_exec python -m rivalcfg -E 3
_exec python -m rivalcfg -E 2
_exec python -m rivalcfg -E 1

_exec python -m rivalcfg -p 125
_exec python -m rivalcfg -p 1000

_exec python -m rivalcfg -s 50
_exec python -m rivalcfg -s 6500

_exec python -m rivalcfg -S 50
_exec python -m rivalcfg -S 6500

_exec python -m rivalcfg -C red
_exec python -m rivalcfg -C f00
_exec python -m rivalcfg -C FF0000
_exec python -m rivalcfg -C "#fF0000"

_exec python -m rivalcfg -r


if [ $_ERROR == 0 ] ; then
    echo -e "\n${_COLOR_SUCCESS}Everything is OK!${_COLOR_NORMAL}";
    exit 0
else
    echo -e "\n${_COLOR_ERROR}$_ERROR error(s)${_COLOR_NORMAL}";
    exit 1
fi
