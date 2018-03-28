#!/bin/bash

echo -e "Executing: ${0}"
set -e
set -o pipefail


# #############################################################################################################
# run

echo "Version Information"

echo -e "\n\nGDB"
gdb --version

echo -e "\n\nGCC"
gcc --version

echo -e "\n\nPython"
python3 --version
