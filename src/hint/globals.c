/*
 * globals.c - Single definition point for all global variables declared
 * in gtlevel.h.  Needed because gtlevel.h is included by multiple .c files;
 * without this file the linker sees multiple definitions of each symbol.
 */

#include "gtlevel.h"

unsigned int  directory[MAXMOVESTOSOLUTION];
int entriesindirectory;
unsigned int  statistics[MAXMOVESTOSOLUTION];
unsigned char mostcomplexsolution;

struct linkedlistboardentry  linkedlist[LINKEDLISTSIZE];
struct linkedlistboardentry *movelist[MOVELISTSIZE];
struct linkedlistboardentry *solution[MAXSOLUTION];
struct linkedlistboardentry *linkedlistpointer;
struct linkedlistboardentry **movelistpointer;
struct linkedlistboardentry *endofboards;
struct linkedlistboardentry *hashtable[HASHTABLESIZE];

struct unpackedboardtype unpackedboard;
int striptypes[12];

/* strips and typedatas are defined with initializers in base.c */
/* gtrafficboard and gtrafficstrips are defined with initializers in gtraffic.c */

unsigned char columninsert1[COLUMNINSERTSIZE];
unsigned char columninsert2[COLUMNINSERTSIZE];
