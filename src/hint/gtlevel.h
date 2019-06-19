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



#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
 
#define MAXSTRIPS 16
#define TRUE 1
#define FALSE 0

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

unsigned int  directory[MAXMOVESTOSOLUTION];
int entriesindirectory;
unsigned int  statistics[MAXMOVESTOSOLUTION];
unsigned char  mostcomplexsolution;



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
struct linkedlistboardentry  linkedlist[LINKEDLISTSIZE];  
struct linkedlistboardentry * movelist[MOVELISTSIZE];

struct linkedlistboardentry * solution[MAXSOLUTION];

struct linkedlistboardentry * linkedlistpointer;   /* initialized in initlinkedlist */
struct linkedlistboardentry **  movelistpointer;   /* initialized in initlinkedlist */

struct linkedlistboardentry * endofboards; /* set in computemoves */
  

struct linkedlistboardentry * hashtable[HASHTABLESIZE];




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

struct {
  int strips[12];
} unpackedboard;

int striptypes[12];

struct gtrafficcar{
    int carpos;
    int carlength;
  };
struct gtrafficcar gtrafficstrips[16][2];


struct strip strips[16];



struct  typedata typedatas[4];

/* index is packedversion of first three rows 3,2,1 (3x4 bits), a column (4 bits) and
   a columnindex (3 bits) */
unsigned char columninsert1[COLUMNINSERTSIZE];

/* index is packedversion of last three rows 6,5,4 (3x4 bits), a column (4 bits) and
   a columnindex (3 bits) */
unsigned char columninsert2[COLUMNINSERTSIZE];

char gtrafficboard[512];


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
