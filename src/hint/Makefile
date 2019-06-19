OBJ=hint.o base.o gtlevel.o gtraffic.o debug.o asci.o precompute.o masterfile.o extract.o 
CFLAGS= -O2 -Wall -ansi -Wstrict-prototypes 
LFLAGS=
CC=gcc
PYTHON=/usr/include/python2.3

_hint.so: $(OBJ) hint_wrap.o
	gcc $(LFLAGS) -shared $(OBJ) hint_wrap.o -o _hint.so 

hint_wrap.c: hint.i
	swig -python hint.i

hint_wrap.o: hint_wrap.c
	$(CC) $(CFLAGS) -c $< -I$(PYTHON)

.c.o:
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f gtlevel
	rm -f *.o
	rm -f core
	rm -f *~
	rm -f *.so




