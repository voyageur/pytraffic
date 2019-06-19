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



/* for use as a module in pyTraffic */
/* Has two functions:
   (1) giving hints
   (2) generating easylevels
*/


#include "gtlevel.h"

/* start of hint part */


static int oldstriptypes[12]={-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};


int newstriptypes(void){
  int i, new;
  new=FALSE;
  for(i=0;i<=11;i++){
    if(striptypes[i]!=oldstriptypes[i]){
      new=TRUE;
    }
  }
  return new;
}
  
void copystriptypes(void){
  int i;
  for(i=0;i<=11;i++){
    oldstriptypes[i]=striptypes[i];
  }
}

int bestmoverows;
int bestmovecolumns;

int getbestmoverows(void){
  return bestmoverows;
}

int getbestmovecolumns(void){
  return bestmovecolumns;
}


void bestmove(int packedrows, int packedcolumns){
  int i;
  struct linkedlistboardentry * l;
  struct linkedlistboardentry * l1;
  struct linkedlistboardentry * lo;
  packedboardtype packedboard;
  packedboard.rows=packedrows;
  packedboard.columns=packedcolumns;
  unpackboard(packedboard);
  for(i=0;i<=11;i++){
    striptypes[i]=strips[unpackedboard.strips[i]].type;
  }
  if (newstriptypes()){
    copystriptypes();
    l=doprep();
    if(l==NULL){
	dumpstrips(stderr);
	fprintf(stderr,"Not enough memory\n");
	exit(-1);
    }
  }
  /* we do too much here! */
  lo=lookupinhashtable(packedboard);
  generatesolution(lo);
  l1=solution[1];
  bestmoverows=(l1->packedboard).rows;
  bestmovecolumns=(l1->packedboard).columns;
}

   
void init(void){
#ifdef FAST
  precompute();
#endif
}

/* start of easy level part */


/* "mailbox globals */
int packedrows;
int packedcolumns;
int bestyoucando;

/* accessor functions */
int getpackedrows(void){
  return packedrows;
}

int getpackedcolumns(void){
  return packedcolumns;
}

int getbestyoucando(void){
  return bestyoucando;
}


/* find a random level with number of moves between
start and end-1 (inclusive)
*/
void findlevel(int start,int end){
  int requestedlevelfound;
  struct linkedlistboardentry * mostcomplicatedlevel;
  int m ;
  requestedlevelfound=FALSE;
  while(!requestedlevelfound){
    randomtypes();
    mostcomplicatedlevel=doprep();
    if(mostcomplicatedlevel!=NULL){
      m=(*mostcomplicatedlevel).movestosolution;
      if(m>=start && m<end){
	requestedlevelfound=TRUE;
	packedrows=(mostcomplicatedlevel->packedboard).rows;
	packedcolumns=(mostcomplicatedlevel->packedboard).columns;
	bestyoucando=m;
      }
    }
  }
}







