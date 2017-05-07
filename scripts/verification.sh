#!/bin/bash

echo -e "Executing: ${0}"
set -e
set -o pipefail


# #############################################################################################################
# variables

FILE_SCRIPT="$(readlink -f $0)"
DIR_SCRIPTS="$(dirname "${FILE_SCRIPT}")"
DIR_PROJECT="${DIR_SCRIPTS}/.."

echo "SYSTEMC_VERSION: ${SYSTEMC_VERSION}"
echo "SYSTEMC_HOME: ${SYSTEMC_HOME}"
echo "DIR_SCRIPTS: ${DIR_SCRIPTS}"
echo "DIR_PROJECT: ${DIR_PROJECT}"


# #############################################################################################################
# run

pushd "${DIR_PROJECT}/verification/"
	python3 main.py
popd
