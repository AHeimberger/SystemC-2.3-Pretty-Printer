#!/usr/bin/python3

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
