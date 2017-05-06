![MIT License](https://img.shields.io/github/license/mashape/apistatus.svg)
![Build Badge Travis](https://travis-ci.org/AHeimberger/SystemC-2.3-Pretty-Printer.svg?branch=master)

## ![SystemC 2.3 Pretty-Printer](./img/logo.svg)

**Goals:**
With the help of <a href="https://sourceware.org/gdb/onlinedocs/gdb/Pretty-Printing.html#Pretty-Printing">GDB Pretty-Printers</a> it is possible to tell GDB how to resolve the data structure to show the value of the object. Without Pretty-Printers the complete structure of the object will be shown with easy to read information.

## Requirements:
- Needs GDB 7.0 or above, which includes support to write Pretty-Printers.
- Linux file system knowledge, terminal operations, root permissions.
- Create the SystemC installation.
- Download and set Pretty-Printers for SystemC 2.3
- Compile and run test program

**Implementation of SystemC datatypes:**
- sc\_bit, sc\_bv\_base,
- sc\_logic, sc\_lv
- sc\_int, sc\_uint, sc\_bigint, sc\_biguint
- sc\_fixed, sc\_ufixed
- sc\_fix, sc\_ufix

**Further Instructions:**
- [Install SystemC 2.3](./SYSTEMC.md)
- [Install Pretty-Printer](./PRETTYPRINTER.md)
- [Verification](./VERIFICATION.md)

**Ressources:**
- [SystemC Pretty-Printer Repository](https://github.com/AHeimberger/SystemC-2.3-Pretty-Printer)
- [Download SystemC 2.3](https://github.com/systemc)
- [Accellera Forum - SystemC 2.3 Pretty-Printer](http://forums.accellera.org/topic/2140-systemc-23-pretty-printer/?hl=pretty-printer)
- [Accellera Forum - Help Debug Information](http://forums.accellera.org/topic/1143-sc-intn/)
- [ricodebug](https://github.com/rainerf/ricodebug)
- [Eclipse](https://www.eclipse.org/)
