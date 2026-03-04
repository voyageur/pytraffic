/*

PyTraffic -- A python simulation of the game Rush Hour invented by
Binary Arts Corporation.

Copyright (C) 2001-2005 Michel Van den Bergh <michel.vandenbergh@uhasselt.be>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING.
If not, write to the Free Software Foundation, Inc.,
59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

*/

#ifndef GTLEVEL_H
#define GTLEVEL_H

#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>

#define MAXSTRIPS 16
/* Use plain 1/0 for boolean values; avoid redefining TRUE/FALSE if already
   defined (e.g. by some system headers). */
#ifndef TRUE
#  define TRUE  1
#endif
#ifndef FALSE
#  define FALSE 0
#endif

#define HASHTABLESIZE 0x40000
#define LINKEDLISTSIZE 150000 
#define MOVELISTSIZE   1500000



#define COLUMNINSERTSIZE 16*16*16*16*8
#define MAXSOLUTION 200
#define MAXMOVESTOSOLUTION 60 
/* we know its 52 ! */
#define MINMOVESTOSOLUTION 21 
/* counting in gtlevel is off by one! */
#define FAST 

extern unsigned int  directory[MAXMOVESTOSOLUTION];
extern int entriesindirectory;
extern unsigned int  statistics[MAXMOVESTOSOLUTION];
extern unsigned char  mostcomplexsolution;



/* typedef struct linkedlistboardentry * linkedlistmoveentry; */


typedef struct{
  unsigned int rows;
  unsigned int columns;
}packedboardtype;

struct linkedlistboardentry{
  packedboardtype packedboard;
  struct linkedlistboardentry ** moves;
  int movestosolution;
};

/* Was  a linked list long ago */
extern struct linkedlistboardentry  linkedlist[LINKEDLISTSIZE];
extern struct linkedlistboardentry * movelist[MOVELISTSIZE];

extern struct linkedlistboardentry * solution[MAXSOLUTION];

extern struct linkedlistboardentry * linkedlistpointer;   /* initialized in initlinkedlist */
extern struct linkedlistboardentry **  movelistpointer;   /* initialized in initlinkedlist */

extern struct linkedlistboardentry * endofboards; /* set in computemoves */


extern struct linkedlistboardentry * hashtable[HASHTABLESIZE];




struct strip {
  int type;
  int  occupancy[6];
  int moves[4];
};




struct typedata {
  int start;
  int end;
  int numberofstrips;
};

struct unpackedboardtype {
  int strips[12];
};
extern struct unpackedboardtype unpackedboard;

extern int striptypes[12];

struct gtrafficcar{
    int carpos;
    int carlength;
  };
extern struct gtrafficcar gtrafficstrips[16][2];


extern struct strip strips[16];



extern struct  typedata typedatas[4];

/* index is packedversion of first three rows 3,2,1 (3x4 bits), a column (4 bits) and
   a columnindex (3 bits) */
extern unsigned char columninsert1[COLUMNINSERTSIZE];

/* index is packedversion of last three rows 6,5,4 (3x4 bits), a column (4 bits) and
   a columnindex (3 bits) */
extern unsigned char columninsert2[COLUMNINSERTSIZE];

extern char gtrafficboard[512];


void showoffset(int offset);

void makestatistics(void);
void makedirectory(void);
void writedirectory(void);
void readdirectory(void);
void makemunch(void);


void testintegritylast(int last);
void testintegritymunch(void);


int lengthofmasterfile(void);

void testintegrity(int start, int end);
void unpackstriptypes(int packedstriptypes);

void printstatistics(void);

void generatemasterfile(void);

int generatesolution(struct linkedlistboardentry * l);

void printsolution(void);

struct  linkedlistboardentry * doprep(void);

int testcompatibilityrowcolmovefast(
				    packedboardtype packedboard,
				    int rowcolnr, 
				    int stripnr);

int testcompatibilityrowmovefast(packedboardtype packedboard,
				 int row, 
				 int stripnr);

int testcompatibilitycolumnmovefast(packedboardtype packedboard,
				    int column, 
				    int stripnr);



packedboardtype insertmove(packedboardtype packedboard, 
			   int rowcol, 
			   int stripnr);


int legaljumpcolumn(int column, int stripnr);
int legaljumprow(int row, int stripnr);



int testcompatibilityforprecompute1(int row3stripnr, 
				    int row2stripnr,
				    int row1stripnr,
				    int columnindex,
				    int columnstripnr);

int testcompatibilityforprecompute2(int row6stripnr,
				    int row5stripnr,
				    int row4stripnr,
				    int columnindex,
				    int columnstripnr);

void precomputecolumninsert1(void);

void precomputecolumninsert2(void);

void precompute(void);


int testcompatibilitycolumnfast(int column, int stripnr);

int equal(packedboardtype p, packedboardtype q);



packedboardtype packboard(void);

void unpackboard(packedboardtype packedboard);

void tophysicalboard(void);

void printphysicalboard(void);

void printcolumninsert1(void);


int testcompatibility(int row, int rowstripnr, int column, int columnstripnr); 

int testcompatibilitycolumn(int column, int stripnr);

int testcompatibilitycolumnpacked(int rows, int column, int stripnr);


int testcompatibilitycolumnmove(int column, int stripnr);

int testcompatibilitycolumnmovepacked(int column, int stripnr);

int testcompatibilityrow(int row, int stripnr);

int testcompatibilityrowpacked(int packedcolumns, int row, int stripnr);

int testcompatibilityrowmove(int row, int stripnr);

int testcompatibilityrowmovepacked(int packedcolumns,int row, int stripnr);

int testcompatibilityrowcol(int rowcolnr, int stripnr);

int testcompatibilityrowcolmove(int rowcolnr, int stripnr);

int findcompatiblecolumn(int column);

int hash(packedboardtype packedboard);

struct linkedlistboardentry *insertinlinkedlist(packedboardtype packedboard);

int searchspace(int rowcolnr);

void inithashtable(void);

void initlinkedlist(void);

int insertinhashtable(packedboardtype packedboard, struct linkedlistboardentry *l);

struct linkedlistboardentry *lookupinhashtable(packedboardtype packedboard);

struct linkedlistboardentry * computemovestosolution(void);

int computemoves(void);

packedboardtype mostcomplicatedlevel(void);

int movestosolution(packedboardtype packedboard);

void randomtypes(void);

void togtrafficboard(int m);

void creategtrafficdeck(int quantity, int treshold);

void dumpstrips(FILE * f);

void printhashtable(void);

void printlinkedlist(void);

void printmoves(void);

void randomboard(void);

void testtypes(void);

double profile(int quantity);

/*
 * Error-signalling mechanism for the Python wrapper.
 * Internal C code calls hint_set_error() instead of exit() to signal a
 * fatal error.  The wrapper checks hint_error_pending() after each call
 * and raises RuntimeError if set.
 */
void hint_set_error(const char *msg);
int  hint_error_pending(void);
const char *hint_error_msg(void);

#endif /* GTLEVEL_H */
