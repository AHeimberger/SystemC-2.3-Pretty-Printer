#!/usr/bin/python3
# Pretty-printers for SystemC23
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

from verification import Verification
from testcases import TestCases
import sys


def main(argv=None):	
    verification = Verification()
    testCases = TestCases(verification)
    testCases.execute()
    verification.closeFile()
    verification.createExecutable()
    verification.executeFile()
    verification.debugFile()
    if not verification.isOk():
        sys.exit(1)


if __name__ == "__main__":
    print("\n")
    main()
