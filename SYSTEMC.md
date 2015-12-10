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
