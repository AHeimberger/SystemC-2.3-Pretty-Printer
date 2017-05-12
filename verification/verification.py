#!/usr/bin/python3
# Pretty-printers for SystemC23
#
# This file was created to create a layer for SystemC testcases.
#
# Copyright (C) 2014 Andreas Heimberger
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------------

import os
import subprocess
import threading
import sys
import time
import re
import filecmp
import difflib

APPLICATION = "./tests/main"
APPLICATION_CODE = "./tests/main.cpp"
FILE_RUN_OUTPUT = "./tests/executed.txt"
FILE_DEBUG_OUTPUT = "./tests/debugged.txt"

# debug application and save gdb print in file
exit = False
def writer(pipe):
    global exit
    mFile = open(FILE_DEBUG_OUTPUT, "w")

    for ln in iter(pipe.stdout.readline, ''):
        if (exit == True):
            break

        s = ln.decode("utf-8")
        if re.match("\(gdb\) \$(?:\d*) = ", s):
            s = re.sub(r"\(gdb\) \$(?:\d*) = ", "", s)
            s = s.replace("\"", "");
            mFile.write(s)

    mFile.close()


# create the main program with different variables
class Verification:
    mFile = 0
    mTestCases = []
    mInternalNumber = 0

    # init main.cpp file
    def __init__(self):
        directory = "./tests"
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.mFile = open(APPLICATION_CODE, "w")
        self.mFile.write("#include <string> \n")
        self.mFile.write("#include <iostream> \n")
        self.mFile.write("#define SC_INCLUDE_FX \n")
        self.mFile.write("#include <systemc.h> \n")
        self.mFile.write("\n")
        self.mFile.write("int sc_main( int, char*[]){ \n");
        self.mFile.write("      // this method is used to turn off warnings for sc_bit which is deprecated \n")
        self.mFile.write("      sc_report_handler::set_actions(\"/IEEE_Std_1666/deprecated\", SC_DO_NOTHING); \n\n")

    # write main.cpp testcases and call std::cout
    def addTestCase(self, testvalue):
        self.mTestCases.append(testvalue)
        self.mFile.write("      std::cout << {0} << std::endl; \n\n".format(testvalue))

    # closing main.cpp file
    def closeFile(self):
        self.mFile.write("      return 0;\n")
        self.mFile.write("}\n")
        self.mFile.write("\n")
        self.mFile.close()

    # create the executabel
    def createExecutable(self):
        SYSTEMC_HOME = os.environ['SYSTEMC_HOME']
        INCPATH = os.path.join(SYSTEMC_HOME, "include")
        LIBPATH = os.path.join(SYSTEMC_HOME, "lib-linux64")
        SOURCEPATH = os.path.join(SYSTEMC_HOME, "lib-linux64")
        print("SYSTEMC_HOME: {0} \nINCPATH: {1} \nLIBPATH: {2} \nSOURCEPATH: {3}".format(SYSTEMC_HOME, INCPATH, LIBPATH, SOURCEPATH))
        os.system("g++ -I. -I {0} -L. -L {1} -Wl,-rpath={2} -o {3} {4} -g -O0 -lsystemc -lm".format(INCPATH, LIBPATH, SOURCEPATH, APPLICATION, APPLICATION_CODE))

    # execute file and write std::cout
    def executeFile(self):
        print("Execute File:")
        print("-"*90)
        if (not os.path.isfile(APPLICATION) and not os.access(APPLICATION, os.X_OK)):
            print("main application does not exist, execute not possible\n\n")
            return
        os.system("{0} > {1}".format(APPLICATION, FILE_RUN_OUTPUT))
        print("\n\n")

    # debug file to get print
    def debugFile(self):
        print("Debug File:")
        print("-"*90)
        sleep = 1
        num_lines = sum(1 for line in open(APPLICATION_CODE))

        if (not os.path.isfile(APPLICATION) and not os.access(APPLICATION, os.X_OK)):
            print("main application does not exist, debug not possible\n\n")
            return

        pipe = subprocess.Popen(["gdb", APPLICATION, "-q"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell=False, bufsize=0)

        th1 = threading.Thread(target=writer, args=(pipe, ))
        th1.start()

        time.sleep(sleep)
        pipe.stdin.write("break {0} \n".format(num_lines-2).encode())

        time.sleep(sleep)
        pipe.stdin.write("run\n".encode())

        time.sleep(sleep)
        print("")

        i = 0;
        maxEntries = len(self.mTestCases)
        for testcase in self.mTestCases:
            time.sleep(sleep)
            pipe.stdin.write("print {0} \n".format(testcase).encode())

            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %d%%  " % ('='*int(50/maxEntries*i), int(100/maxEntries*i)))
            sys.stdout.flush()
            i += 1

        time.sleep(sleep)
        pipe.stdin.write("quit\n".encode())

        global exit
        exit = True
        time.sleep(sleep)
        print("\n\n")

    # comparing files to see difference between pretty printer and sdt::cout print
    def isOk(self):
        print("Compare Files:")
        print("-"*90)

        file1 = open(FILE_RUN_OUTPUT, "r")
        file2 = open(FILE_DEBUG_OUTPUT, "r")
        errorcnt = 0

        num_lines1 = sum(1 for line in file1)
        num_lines2 = sum(1 for line in file2)
        lines_to_read = num_lines1 if (num_lines1 < num_lines2) else num_lines2
        file1.seek(0)
        file2.seek(0)

        verificationIsOk = True

        if num_lines1 < num_lines2:
            print("Failure files are not congruent in number of lines.")
            verificationIsOk = False

        for i in range(0, lines_to_read, 1):
            file1_line = file1.readline().rstrip()
            file2_line = file2.readline().rstrip()
            if file1_line != file2_line:
                print("Failure in line number: {0} \n   - Expected: {1}\n   - Result was: {2}".format(str(i+1), file1_line, file2_line))
                verificationIsOk = False

        if verificationIsOk:
            print("Files are congruent.")

        file1.close()
        file2.close()
        return verificationIsOk

    # creates an internal variable name and stores it within a list of variablenames for debug
    def createVariableName(self, strVarName):
        self.mInternalNumber += 1;
        varName = strVarName + str(self.mInternalNumber)
        return varName

    # ------------------------------------------------------------------------------------------

    # create variables
    def std_string(self, value):
        varName = self.createVariableName("std_string_")
        self.mFile.write("      std::string {0} = \"{1}\"; \n".format(varName, value))
        self.addTestCase(varName)

    def sc_bit(self, value):
        varName = self.createVariableName("sc_bit_")
        self.mFile.write("      sc_bit {0}; \n".format(varName))
        self.mFile.write("      {0} = {1}; \n".format(varName, value))
        self.addTestCase(varName)

    def sc_bv(self, size, value):
        varName = self.createVariableName("sc_bv_")
        self.mFile.write("      sc_bv<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_logic(self, value):
        varName = self.createVariableName("sc_logic_")
        self.mFile.write("      sc_logic {0}; \n".format(varName))
        self.mFile.write("      {0} = {1}; \n".format(varName, value))
        self.addTestCase(varName)

    def sc_lv(self, size, value):
        varName = self.createVariableName("sc_lv_")
        self.mFile.write("      sc_lv<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_int(self, size, value):
        #maxiumum 1 <= size <= 64
        varName = self.createVariableName("sc_int_")
        self.mFile.write("      sc_int<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_uint(self, size, value):
        varName = self.createVariableName("sc_uint_")
        self.mFile.write("      sc_uint<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_bigint(self, size, value):
        varName = self.createVariableName("sc_bigint_")
        self.mFile.write("      sc_bigint<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_biguint(self, size, value):
        varName = self.createVariableName("sc_biguint_")
        self.mFile.write("      sc_biguint<{0}> {1} = {2}; \n".format(str(size), varName, value))
        self.addTestCase(varName)

    def sc_fixed(self, size1, size2, value, mod1=None, mod2=None):
        varName = self.createVariableName("sc_fixed_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_fixed<{0}, {1}, {2}, {3}> {4} = {5}; \n".format(str(size1), str(size2), str(mod1), str(mod2), varName, value))
        else:
            self.mFile.write("      sc_fixed<{0}, {1}> {2} = {3}; \n".format(str(size1), str(size2), varName, value))
        self.addTestCase(varName)

    def sc_ufixed(self, size1, size2, value, mod1=None, mod2=None):
        varName = self.createVariableName("sc_ufixed_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_ufixed<{0}, {1}, {2}, {3}> {4} = {5}; \n".format(str(size1), str(size2), str(mod1), str(mod2), varName, value))
        else:
            self.mFile.write("      sc_ufixed<{0}, {1}> {2} = {3}; \n".format(str(size1), str(size2), varName, value))
        self.addTestCase(varName)

    def sc_fix(self, size1, size2, value,  mod1=None, mod2=None):
        varName = self.createVariableName("sc_fix_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_fix {0} ({1}, {2}, {3}, {4}); \n".format(varName, str(size1), str(size2), str(mod1), str(mod2)))
            self.mFile.write("      {0} = {1}; \n".format(varName, value))
        else:
            self.mFile.write("      sc_fix {0} ({1}, {2}); \n".format(varName, str(size1), str(size2)))
            self.mFile.write("      {0} = {1}; \n".format(varName, value))
        self.addTestCase(varName)

    def sc_ufix(self, size1, size2, value,  mod1=None, mod2=None):
        varName = self.createVariableName("sc_ufix_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_ufix {0} ({1}, {2}, {3}, {4}); \n".format(varName, str(size1), str(size2), str(mod1), str(mod2)))
            self.mFile.write("      {0} = {1}; \n".format(varName, value))
        else:
            self.mFile.write("      sc_ufix {0} ({1}, {2}); \n".format(varName, str(size1), str(size2)))
            self.mFile.write("      {0} = {1}; \n".format(varName, value))
        self.addTestCase(varName)

