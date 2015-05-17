## Requirements:
- Needs GDB 7.0 or above, which includes support to write Pretty-Printers.
- Linux file system knowledge, terminal operations, root permissions.
- Create the SystemC installation.
- Download and set Pretty-Printers for SystemC 2.3
- Compile and run test program


## Installing SystemC 2.3:
It's always better to see the installing instructions <a href="https://github.com/funningboy/systemc-2.3.0/blob/master/INSTALL">INSTALL</a> given by the authors of SystemC. Nevertheless, I will show you the steps I did. Before calling make it's a good idea to open the Makefile with gedit and search for the entry prefix. If the prefix is set to /usr/local/systemc23 the entry was accepted correctly. The last command checks your SystemC installation and shows you, if everything went correct during install.</p>

**Download SystemC2.3**
```sh
cd ~
git clone https://github.com/systemc/systemc-2.3.git
chmod  -R +x systemc-2.3
cd systemc-2.3
mkdir objdir
cd objdir
sudo mkdir /usr/local/systemc23
export CXX=g++
../configure --prefix=/usr/local/systemc23
make
sudo make install
make check
```

As described in <a href="https://github.com/funningboy/systemc-2.3.0/blob/master/INSTALL">INSTALL</a> it is your decision if you leave your objdir folder or not. Later on you can use make to uninstall SystemC.

The following command adds your SystemC directory to the export environment variables. Doing this from the command line will not add the environment variable permanently. Therefore after a logout or closing the shell the variable is lost. To add environment variables permanently see <a href="http://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables">following link</a>. In my case I added a <b>systemc23.sh</b> file to the <b>/etc/profile.d/</b> directory which contains following assignment. Eventually you need a relog.

```sh
cd /etc/profile.d/
sudo gedit systemc23.sh
```

Add following entry to the file:

```sh
export SYSTEMC_HOME=/usr/local/systemc23
```

Reboot your linux distribution to load the environment variable.

```sh
sudo reboot
```

The next command checks your Linux system if the environment variable is set.

```sh
printenv | grep SYSTEMC
## SYSTEMC_HOME=/usr/local/systemc23
```

## Installing Pretty-Printer:
Currently you installed only a version of SystemC. With this shared libraries you are not able to see the value/s stored within an object. The interesting part will come now. I provide a git directory which contains multiple folders with example applications, the python Pretty-Printer and the python printers test interface. Furthermore, we install some dependencies for Python3.

```sh
cd ~
git clone https://github.com/AHeimberger/SystemC-2.3-Pretty-Printer.git
mv SystemC-2.3-Pretty-Printer systemc23-pretty-printer
sudo apt-get install python3 python3-pip
python3 -m pip install numpy
gedit .gdbinit
```

In the next step we have to modify the .gdbinit file in the home directory. This file is loaded by GDB at the start of the debug session. It depends upon your linux version whether this file already exists or not. If this file exists to print datatypes of the <a href="https://sourceware.org/gdb/wiki/STLSupport">standard template library</a>, ensure  this file imports also os, creates a variable to your home directory and registers the Pretty-Printer for SystemC.

```python
python
import sys, os

home = os.path.expanduser("~")

sys.path.insert(0, home + '/systemc23-pretty-printer/systemc23/')
from systemc23printers import register_systemc23_printers
register_systemc23_printers (None)

end
```

Next, we start GDB in the terminal and check if all Pretty-Printers were loaded correctly.

```sh
gdb
info pretty-printer
#    .*
#    bound
#    SystemC23
#    sc_bigint
#    sc_biguint
#    sc_bit
#    sc_bv_base
#    sc_fix
#    sc_fixed
#    sc_int
#    sc_lv
#    sc_logic
#    sc_ufix
#    sc_ufixed
#    sc_uint
```

**Build an example project:**
Together with the SystemC Pretty-Printer you downloaded a folder called "example", which contains test files to pretty-print SystemC Datatypes. We will now build one of this example files and see if operation of the Pretty-Printer works correctly. See the Makefile within the example directory to get information about building your own projects.

```sh
cd ~
cd systemc-pretty-printer/example/Datatypes
make
```

In the next step we will start gdb and print datatypes.

```sh
gdb main
break 152
run
print test13_3
# watch the value using the pretty-printer
disable pretty-printer
print test13_3
# value of test13_3 without using the pretty-printer
enable pretty-printer
print test13_3
# watch the value using the pretty-printer
quit
```
