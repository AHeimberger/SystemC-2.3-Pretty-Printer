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

# debug application and save gdb print in file
exit = False
def writer(pipe):
    global exit
    mFile = open("./tests/debugged.txt", "w")

    for ln in iter(pipe.stdout.readline, ''):
        if (exit == True):
            break

        s = ln.decode("utf-8")
        if re.match("\(gdb\) \$(?:\d*) = ", s):
            s = re.sub(r"\(gdb\) \$(?:\d*) = ", "", s)
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

        self.mFile = open("./tests/main.cpp", "w")
        self.mFile.write("#include <string> \n")
        self.mFile.write("#include <iostream> \n")
        self.mFile.write("#define SC_INCLUDE_FX \n")
        self.mFile.write("#include <systemc.h> \n")
        self.mFile.write("\n")
        self.mFile.write("int sc_main( int, char*[]){ \n");
        self.mFile.write("      // this method is used to turn off warnings for sc_bit which is deprecated \n")
        self.mFile.write("      sc_report_handler::set_actions(\"/IEEE_Std_1666/deprecated\", SC_DO_NOTHING); \n\n")

    # write main.cpp testcases and call std::cout
    def createIOStream(self, testcase):
        self.mTestCases.append(testcase)
        self.mFile.write("      std::cout << " + testcase +  " << std::endl; \n\n")

    # closing main.cpp file
    def closeFile(self):
        self.mFile.write("      return 0;\n")
        self.mFile.write("}\n")
        self.mFile.write("\n")
        self.mFile.close()

    # create the executabel
    def createExecutable(self):
        SYSTEMC_HOME = os.environ['SYSTEMC_HOME']
        INCPATH = os.path.join(SYSTEMC_HOME, "/include")
        LIBPATH = os.path.join(SYSTEMC_HOME, "/lib-linux64")
        SOURCEPATH = os.path.join(SYSTEMC_HOME, "/lib-linux64")
        os.system("g++ -I. -I" + INCPATH + " -L. -L" + LIBPATH + " -Wl,-rpath=" + SOURCEPATH + " -o ./tests/main ./tests/main.cpp -g -O0 -lsystemc -lm")

    # execute file and write std::cout
    def executeFile(self):
        print("Execute File :")
        print("-"*90)
        os.system("./tests/main > ./tests/executed.txt")

    # debug file to get print
    def debugFile(self):
        print("Debug File :")
        print("-"*90)
        sleep = 1
        num_lines = sum(1 for line in open('./tests/main.cpp'))

        #fw = open("comp2.txt", "w")
        pipe = subprocess.Popen(["gdb", "./tests/main", "-q"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, shell=False, bufsize=0)

        th1 = threading.Thread(target=writer, args=(pipe, ))
        th1.start()

        time.sleep(sleep)
        pipe.stdin.write(bytes("break " + str(num_lines-2) + "\n"))

        time.sleep(sleep)
        pipe.stdin.write(bytes("run\n"))

        for testcase in self.mTestCases:
            time.sleep(sleep)
            pipe.stdin.write(bytes("print " + testcase + "\n"))

        time.sleep(sleep)
        pipe.stdin.write(bytes("quit\n"))

        global exit
        exit = True
        time.sleep(sleep)

    # comparing files to see difference between pretty printer and sdt::cout print
    def compareFiles(self):
        print("Compare Files :")
        print("-"*90)

        file1 = open("./tests/executed.txt", "r")
        file2 = open("./tests/debugged.txt", "r")
        errorcnt = 0

        num_lines1 = sum(1 for line in file1)
        num_lines2 = sum(1 for line in file2)
        lines_to_read = num_lines1 if (num_lines1 < num_lines2) else num_lines2
        file1.seek(0)
        file2.seek(0)

        if num_lines1 < num_lines2:
            print("Failure files are not congruent in number of lines.")

        for i in range(0, lines_to_read, 1):
            file1_line = file1.readline().rstrip()
            file2_line = file2.readline().rstrip()
            if file1_line != file2_line:
                print("Failure in line number: " + str(i+1) + " expected: " + file1_line + " result was: " + file2_line)
                break

        print ("Happy : All testcases are congruent.")
        file1.close()
        file2.close()

    # creates an internal variable name and stores it within a list of variablenames for debug
    def createVariableName(self, strVarName):
        self.mInternalNumber += 1;
        varName = strVarName + str(self.mInternalNumber)
        return varName

    # ------------------------------------------------------------------------------------------

    # create variables
    def sc_bit(self, value):
        varName = self.createVariableName("sc_bit_")
        self.mFile.write("      sc_bit " + varName + "; \n")
        self.mFile.write("      " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_bv(self, size, value):
        varName = self.createVariableName("sc_bv_")
        self.mFile.write("      sc_bv<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_logic(self, value):
        varName = self.createVariableName("sc_logic_")
        self.mFile.write("      sc_logic " + varName + "; \n")
        self.mFile.write("      " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_lv(self, size, value):
        varName = self.createVariableName("sc_lv_")
        self.mFile.write("      sc_lv<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_int(self, size, value):
        #maxiumum 1 <= size <= 64
        varName = self.createVariableName("sc_int_")
        self.mFile.write("      sc_int<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_uint(self, size, value):
        varName = self.createVariableName("sc_uint_")
        self.mFile.write("      sc_uint<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_bigint(self, size, value):
        varName = self.createVariableName("sc_bigint_")
        self.mFile.write("      sc_bigint<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_biguint(self, size, value):
        varName = self.createVariableName("sc_biguint_")
        self.mFile.write("      sc_biguint<" + str(size) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_fixed(self, size1, size2, value, mod1=None, mod2=None):
        varName = self.createVariableName("sc_fixed_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_fixed<" + str(size1) + ", " + str(size2) + ", " + str(mod1) + ", " + str(mod2) + "> " + varName + " = " + value + "; \n")
        else:
            self.mFile.write("      sc_fixed<" + str(size1) + ", " + str(size2) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_ufixed(self, size1, size2, value, mod1=None, mod2=None):
        varName = self.createVariableName("sc_ufixed_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_ufixed<" + str(size1) + ", " + str(size2) + ", " + str(mod1) + ", " + str(mod2) + "> " + varName + " = " + value + "; \n")
        else:
            self.mFile.write("      sc_ufixed<" + str(size1) + ", " + str(size2) + "> " + varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_fix(self, size1, size2, value,  mod1=None, mod2=None):
        varName = self.createVariableName("sc_fix_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_fix " + varName + "(" + str(size1) + ", " + str(size2) + ", " + str(mod1) + ", " + str(mod2) + ");")
            self.mFile.write(varName + " = " + value + "; \n")
        else:
            self.mFile.write("      sc_fix " + varName + "(" + str(size1) + ", " + str(size2) + ");")
            self.mFile.write(varName + " = " + value + "; \n")
        self.createIOStream(varName)

    def sc_ufix(self, size1, size2, value,  mod1=None, mod2=None):
        varName = self.createVariableName("sc_ufix_")
        if (mod1 != None and mod2 != None):
            self.mFile.write("      sc_ufix " + varName + "(" + str(size1) + ", " + str(size2) + ", " + str(mod1) + ", " + str(mod2) + ");")
            self.mFile.write(varName + " = " + value + "; \n")
        else:
            self.mFile.write("      sc_ufix " + varName + "(" + str(size1) + ", " + str(size2) + ");")
            self.mFile.write(varName + " = " + value + "; \n")
        self.createIOStream(varName)

