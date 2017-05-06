#!/bin/bash

echo -e "Executing: ${0}"
set -e
set -o pipefail


# #############################################################################################################
# variables

DIR_SCRIPTS="${DIR_PROJECT}/scripts"


# #############################################################################################################
# functions

function commands
{
	echo "Following commands exist:"
	echo "- help"

	for fname in ${DIR_SCRIPTS}/*.sh; do
		echo "-" ${fname} | sed "s@${DIR_SCRIPTS}/@@" | sed "s@.sh@@"
	done
}

# #############################################################################################################
# run

if [ -z $1 ] || [ $1 == "help" ] ; then
	commands
elif [ -f ${DIR_SCRIPTS}/$1.sh ] ; then
	${DIR_SCRIPTS}/$1.sh
elif [ $# == 1 ] && [ -e $1 ]; then
	$1
else
	echo "Command " $1 " not found."
	commands
	exit 1;
fi
