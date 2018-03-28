![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/AHeimberger/SystemC-2.3-Pretty-Printer.svg?branch=master)](https://travis-ci.org/AHeimberger/SystemC-2.3-Pretty-Printer)

## ![SystemC 2.3 Pretty-Printer](./img/logo.png)

**Goals:**
With the help of <a href="https://sourceware.org/gdb/onlinedocs/gdb/Pretty-Printing.html#Pretty-Printing">GDB Pretty-Printers</a> it is possible to tell GDB how to resolve the data structure to show the value of the object. Without Pretty-Printers the complete structure of the object will be shown.

**Requirements:**
- Needs GDB 7.0 or above, which includes support to write Pretty-Printers.
- Create the SystemC installation. [See install SystemC 2.3](./documentation/SystemC.md)
- Download and set Pretty-Printers for SystemC 2.3. [See install Pretty-Printer](./documentation/PrettyPrinter.md)
- Compile and run test program. [See verification](./documentation/Verification.md)

**Supported datatypes:**
- sc\_bit, sc\_bv\_base,
- sc\_logic, sc\_lv
- sc\_fixed, sc\_ufixed
- sc\_fix, sc\_ufix
- sc\_int, sc\_uint
- sc\_bigint, sc\_biguint

**Docker Execution**

    docker build -t systemc .
    docker run --rm=true systemc version
    docker run --rm=true --security-opt seccomp=unconfined systemc verification

**Ressources:**
- [Download SystemC 2.3](http://accellera.org/downloads/standards/systemc)
- [Accellera Forum - SystemC 2.3 Pretty-Printer](http://forums.accellera.org/topic/2140-systemc-23-pretty-printer/?hl=pretty-printer)
