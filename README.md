## ![SystemC 2.3 Pretty Printer](./img/logo.png)

**Goals:**
Currently GDB can not show the value/s stored within the object, because it has now knowledge about the data-structure. With the help of <a href="https://sourceware.org/gdb/onlinedocs/gdb/Pretty-Printing.html#Pretty-Printing">GDB pretty printers</a> it is possible to tell GDB how to resolve the data structure to show the value of the object. Without pretty printers the complete structure of the object will be shown with no valuable information.

**Implementation of SystemC datatypes:**
- sc\_bit, sc\_bv\_base,
- sc\_logic, sc\_lv
- sc\_int, sc\_uint, sc\_bigint, sc\_biguint
- sc\_fixed, sc\_ufixed
- sc\_fix, sc\_ufix

**Further Instructions:**
- [Usage](./USAGE.md)
- [Verification](./VERIFICATION.md)
