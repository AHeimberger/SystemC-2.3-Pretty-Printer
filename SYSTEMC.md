## Installing SystemC:
It's always better to see the installing instructions INSTALL given by the authors of SystemC. Nevertheless, I will show you the steps I did. Before calling make it's a good idea to open the Makefile with gedit and search for the entry prefix. If the prefix is set to /usr/local/systemc23 the entry was accepted correctly. The last command checks your SystemC installation and shows you, if everything went correct during install.</p>

**Download SystemC**<br/>
[http://accellera.org/downloads/standards/systemc]

```sh
SYSTEMC_VERSION=systemc-2.3.0a
cd /tmp
wget http://accellera.org/images/downloads/standards/systemc/${SYSTEMC_VERSION}.tar.gz
tar xvf ${SYSTEMC_VERSION}.tar.gz
rm ${SYSTEMC_VERSION}.tar.gz
cd ${SYSTEMC_VERSION}
mkdir objdir
cd objdir
export CXX=g++
../configure --prefix=${SYSTEMC_HOME}
make
make install
make check
cd ../..
rm -rf ${SYSTEMC_VERSION}
```

As described in INSTALL it is your decision if you leave your objdir folder or not. Later on you can use make to uninstall SystemC.

The following command adds your SystemC directory to the export environment variables. Doing this from the command line will not add the environment variable permanently. Therefore after a logout or closing the shell the variable is lost. To add environment variables permanently see <a href="http://unix.stackexchange.com/questions/117467/how-to-permanently-set-environmental-variables">following link</a>. In my case I added a <b>systemc23.sh</b> file to the <b>/etc/profile.d/</b> directory which contains following assignment. Eventually you need a relog.

```sh
cd /etc/profile.d/
sudo gedit systemc.sh
```

Add following entry to the file:

```sh
export SYSTEMC_VERSION=systemc-2.3.0a
export SYSTEMC_HOME=/opt/${SYSTEMC_VERSION}
```

Reboot to ensure variables are set permanently.

```sh
sudo reboot -h now
```

The next command checks if the environment variable is set.

```sh
echo ${SYSTEMC_VERSION}
echo ${SYSTEMC_HOME}
```
