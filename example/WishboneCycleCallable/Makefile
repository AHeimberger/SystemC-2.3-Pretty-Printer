CC = g++
CFLAGS  = -Wall -g
LDFLAGS = -lm -lsystemc
SOURCES = master.cpp memory.cpp main.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = main.out

INCPATH = $(SYSTEMC_HOME)/include
LIBPATH = $(SYSTEMC_HOME)/lib-linux64
SOURCEPATH = $(SYSTEMC_HOME)/lib-linux64

INCLUDES = -I. -I$(INCPATH) -L. -L$(LIBPATH) -Wl,-rpath=$(SOURCEPATH)

all : main.o master.o memory.o
	${CC} $(INCLUDES) ${CFLAGS} main.o master.o memory.o ${LDFLAGS} -o main.out

main.o : main.cpp top.h
	$(CC) $(INCLUDES) $(CFLAGS) -c main.cpp $(LDFLAGS)

master.o : master.cpp master.h defines.h
	$(CC) $(INCLUDES) $(CFLAGS) -c master.cpp $(LDFLAGS)

memory.o : memory.cpp memory.h defines.h
	$(CC) $(INCLUDES) $(CFLAGS) -c memory.cpp $(LDFLAGS)

clean:
	rm -rf *o $(EXECUTABLE)
