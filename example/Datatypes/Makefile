INCPATH = $(SYSTEMC_HOME)/include
LIBPATH = $(SYSTEMC_HOME)/lib-linux64
SOURCEPATH = $(SYSTEMC_HOME)/lib-linux64

main: main.cpp
	g++ -I. -I$(INCPATH) -L. -L$(LIBPATH) -Wl,-rpath=$(SOURCEPATH) -o main.out main.cpp -g -O0 -lsystemc -lm

clean:
	rm -rf *o main.out
