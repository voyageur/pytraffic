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



#include "gtlevel.h"


struct strip strips[16]=
{
  {0,{0,0,0,0,0,0},{0,0,0,0}},       /* 0 */
  {1,{1,1,0,0,0,0},{2,3,4,5}},       /* 1 */
  {1,{0,1,1,0,0,0},{1,3,4,5}},       /* 2 */
  {1,{0,0,1,1,0,0},{1,2,4,5}},       /* 3 */
  {1,{0,0,0,1,1,0},{1,2,3,5}},       /* 4 */
  {1,{0,0,0,0,1,1},{1,2,3,4}},       /* 5 */
  {2,{1,1,1,0,0,0},{7,8,9,0}},       /* 6 */ 
  {2,{0,1,1,1,0,0},{6,8,9,0}},       /* 7 */
  {2,{0,0,1,1,1,0},{6,7,9,0}},       /* 8 */
  {2,{0,0,0,1,1,1},{6,7,8,0}},       /* 9 */
  {3,{1,1,2,2,0,0},{11,12,0,0}},      /* 10 */
  {3,{1,1,0,2,2,0},{10,12,13,0}},    /* 11 */
  {3,{1,1,0,0,2,2},{10,11,14,15}},     /* 12 */
  {3,{0,1,1,2,2,0},{11,14,0,0}},     /* 13 */
  {3,{0,1,1,0,2,2},{12,13,15,0}},    /* 14 */
  {3,{0,0,1,1,2,2},{12,14,0,0}}      /* 15 */
};
struct  typedata typedatas[4]=
{
  {0,0,0},
  {1,5,1},
  {6,9,1},
  {10,15,2}
};


/* return 0 is there is a solution, -1 otherwise */
int generatesolution(struct linkedlistboardentry * l){
  int movestosolution=(*l).movestosolution;
  int i=0;
  struct linkedlistboardentry ** p;
  int nosolution=FALSE;
  solution[i]=l;
  i++;
  while((movestosolution>1)||nosolution){
    p=(*l).moves;
    nosolution=TRUE;
    if(p!=NULL){
      while(((*p)!=NULL)&&nosolution){
	if((**p).movestosolution==movestosolution-1){
	  nosolution=FALSE;
	  movestosolution--;
	  solution[i]=*p;

	  i++;
	  if(i==MAXSOLUTION){
	    fprintf(stderr,"Solution to big\n");
	    dumpstrips(stderr);
	    exit(-1);
	  }
	  l=*p;
	}else{
	  p++;
	}
      }
    }
  }
  if(nosolution){
    return -1;
  }else{
    return 0;
  }
}

/* returns TRUE if no jump, or if jump is legal */
int legaljumpcolumn(int column, int stripnr)
{
  int blockingrow1, blockingrow2, originalstripnr;
    /* hack */
  if(strips[stripnr].type==1){
    originalstripnr=unpackedboard.strips[column+6];
    if(abs(stripnr-originalstripnr)>=3){
      blockingrow1=unpackedboard.strips[2];
      blockingrow2=unpackedboard.strips[3];
      if((strips[blockingrow1].occupancy[column]==0)
	 &&(strips[blockingrow2].occupancy[column]==0)){
	return TRUE;
      }else{return FALSE;}
    }else{return TRUE;}
  }else{return TRUE;}
}


/* returns TRUE of no jump, or if jump is legal */
int legaljumprow(int row, int stripnr){
  int blockingcolumn1, blockingcolumn2, originalstripnr;
  if(strips[stripnr].type==1){
    originalstripnr=unpackedboard.strips[row];
    if(abs(stripnr-originalstripnr)>=3){
      blockingcolumn1=unpackedboard.strips[8];
      blockingcolumn2=unpackedboard.strips[9];
      if((strips[blockingcolumn1].occupancy[row]==0)
	 &&(strips[blockingcolumn2].occupancy[row]==0)){
	return TRUE;
      }else{return FALSE;}
    }else{return TRUE;}
  }else{return TRUE;}
}

/* return a hash function with 18 bits */
int hash(packedboardtype packedboard){
  return (((packedboard.rows *0x43212347)+(packedboard.columns *0x53643478))
	  >>14);
}

int equal(packedboardtype p, packedboardtype q){
  return((p.rows==q.rows)&&(p.columns==q.columns));
}

/* returns -1 if hashtable is full */
int insertinhashtable(packedboardtype packedboard, struct linkedlistboardentry *l){
  packedboardtype packedboard1;
  int hashed,originalhashed;
  int inserted=FALSE;
  int collision;
  struct linkedlistboardentry *ll;
  collision=0;
  hashed=hash(packedboard);
  originalhashed=hashed;
  while(!inserted){
    ll=hashtable[hashed];
    if(ll==NULL){
      hashtable[hashed]=l;
      hashed=hash(packedboard);


      inserted=TRUE;
    }else{
      packedboard1=(*ll).packedboard;
      if(equal(packedboard,packedboard1)){
        fprintf(stderr,"Error: trying to insert %d%d twice\n",packedboard.rows,packedboard.columns);
	dumpstrips(stderr);
	exit(-1);
      }else{
	hashed++;
	if(hashed==HASHTABLESIZE){
	  hashed=0;
	}
	collision++;
      }
      if(hashed==originalhashed){
	return -1;
      }
    }
  }
  return collision;
}

struct linkedlistboardentry * doprep(void){
  int sp,c;
  inithashtable();
  initlinkedlist();
  sp=searchspace(0);
  if(sp!=0 && sp!=-1){
    c=computemoves();
    if(c!=-1){
      return computemovestosolution();
    }
  }
  return NULL;
}


/* test if a given rowstripnr and columstripnr are compatible for
   the indicated row and column */

int testcompatibility(int row, int rowstripnr, int column, int columnstripnr)
{
  if((strips[rowstripnr].occupancy[column]!=0) 
     && (strips[columnstripnr].occupancy[row]!=0)){
        return FALSE;
  }else{
        return TRUE;
  }
}





/* checks is a column with given stripnr can be inserted with already
   given rows */   
int testcompatibilitycolumn(int column, int stripnr)
{
    int goodstripnr=TRUE;
    int row;
    for(row=0;row<=5;row++){
      if(!testcompatibility(row,unpackedboard.strips[row],column,stripnr)){
	goodstripnr=FALSE;
      }
    }
    return goodstripnr;
}

#ifdef FAST
int testcompatibilitycolumnfast(int column, int stripnr)
{
  int packedrows1,packedrows2;
  packedrows1=(unpackedboard.strips[2]<<15)+
    (unpackedboard.strips[1]<<11)+
    (unpackedboard.strips[0]<<7)+
    (stripnr<<3)+column;
  packedrows2=(unpackedboard.strips[5]<<15)+
    (unpackedboard.strips[4]<<11)+
    (unpackedboard.strips[3]<<7)+
    (stripnr<<3)+column;
  return  (columninsert1[packedrows1]) &&   (columninsert2[packedrows2]);          
}
#endif







/* checks if a column move with given stripnr is legal. Almost identical
to testcompatibilitycolumn
*/   

int testcompatibilitycolumnmove(int column, int stripnr)
{
  return testcompatibilitycolumn(column,stripnr) && legaljumpcolumn(column,  stripnr);
}

#ifdef FAST
int testcompatibilitycolumnmovefast(packedboardtype packedboard, int column, int stripnr)
{
  int packedrows321, packedrows654;
  packedrows321=((((packedboard.rows & 0xFFF)<<4)+stripnr)<<3) +column;
  packedrows654=(((((packedboard.rows &0xFFF000)>>12)<<4)+stripnr)<<3)+column;
  /* debug
  c=columninsert1[packedrows321]&&columninsert2[packedrows654];
  if(c!=testcompatibilitycolumn(column,stripnr)){
    printf("Problem in testcompatibilitycolumnmovefast\n");
    printf("packedrows321=%x packedrows654=%x\n",packedrows321>>3, packedrows654>>3);
    printf("column=%d stripnr=%d\n",column,stripnr);
    tophysicalboard();
    printphysicalboard();
  }
   debug */    


  if(columninsert1[packedrows321]&&columninsert2[packedrows654]){
    return legaljumpcolumn(column,stripnr);
  }else{
    return FALSE;
  }
  
}

#endif






/* similar to previous functions */
int testcompatibilityrow(int row, int stripnr)
{
    int goodstripnr=TRUE;
    int column;
    for(column=0;column<=5;column++){
      if(!testcompatibility(row,stripnr,column,
                        unpackedboard.strips[column+6])){
	goodstripnr=FALSE;
      }
    }
    return goodstripnr;
}

#ifdef FAST
int testcompatibilityrowfast(int row, int stripnr)
{
  int packedcolumns1,packedcolumns2;
  packedcolumns1=(unpackedboard.strips[8]<<15)+
    (unpackedboard.strips[7]<<11)+
    (unpackedboard.strips[6]<<7)+
    (stripnr<<3)+row;
  packedcolumns2=(unpackedboard.strips[11]<<15)+
    (unpackedboard.strips[10]<<11)+
    (unpackedboard.strips[9]<<7)+
    (stripnr<<3)+row;
  return  (columninsert1[packedcolumns1]) &&   (columninsert2[packedcolumns2]);          
}
#endif



int testcompatibilityrowmove(int row, int stripnr)
{
  return testcompatibilityrow(row,stripnr)&& legaljumprow(row,stripnr);
}

#ifdef FAST
int testcompatibilityrowmovefast(packedboardtype packedboard, 
				 int row, 
				 int stripnr)
{
  int packedcolumns321, packedcolumns654;
  packedcolumns321=((((packedboard.columns & 0xFFF)<<4)+stripnr)<<3) +row;
  packedcolumns654=(((((packedboard.columns &0xFFF000)>>12)<<4)
		     +stripnr)<<3)+row;
  if(columninsert1[packedcolumns321]&&columninsert2[packedcolumns654]){
    return legaljumprow(row,stripnr);
  }else{
    return FALSE;
  }
}

#endif




int testcompatibilityrowcol(int rowcolnr, int stripnr){
  if(rowcolnr<=5){
    return testcompatibilityrow(rowcolnr,stripnr);
  }else{
    return testcompatibilitycolumn(rowcolnr-6,stripnr);
  }
}


int testcompatibilityrowcolmove(int rowcolnr, int stripnr){
  if(rowcolnr<=5){
    return testcompatibilityrowmove(rowcolnr,stripnr);
  }else{
    return testcompatibilitycolumnmove(rowcolnr-6,stripnr);
  }
}
#ifdef FAST
int testcompatibilityrowcolmovefast(packedboardtype packedboard,
				    int rowcolnr, 
				    int stripnr){
  if(rowcolnr<=5){
    return testcompatibilityrowmovefast(packedboard,
					rowcolnr,
					stripnr);
  }else{
    return testcompatibilitycolumnmovefast(packedboard,
					   rowcolnr-6,
					   stripnr);
  }
}
#endif








/* find a column compatible with already determined rows */

int findcompatiblecolumn(int column){
  int compatiblecolumnfound=FALSE;
  int teststripnr;
  while(compatiblecolumnfound==FALSE){
    teststripnr=floor((rand()*16.0/(RAND_MAX+1.0)));
    compatiblecolumnfound=testcompatibilitycolumn(column, teststripnr);
    }

  return teststripnr;
}



/* packs a board
*/

packedboardtype packboard(){
  packedboardtype packing={0,0};
  int i;
    for(i=5;i>=0;i--){
    packing.rows=(packing.rows<<4)+unpackedboard.strips[i];
    }
    for(i=11;i>=6;i--){
    packing.columns=(packing.columns<<4)+unpackedboard.strips[i];
    }
    return packing;
}

/* opposite of the previous function */
void unpackboard(packedboardtype packedboard){
  int i;
  int r,c;
  r=packedboard.rows;
  c=packedboard.columns;
  for(i=0;i<=5;i++){
    unpackedboard.strips[i]=(r & 0xF);
    r>>=4;
  }
  for(i=6;i<=11;i++){
    unpackedboard.strips[i]=(c & 0xF);
    c>>=4;
  }

}



 

/* returns NULL if linkedlist is full */

struct linkedlistboardentry *insertinlinkedlist(packedboardtype packedboard){
  struct linkedlistboardentry * l
         = linkedlistpointer;
  (*linkedlistpointer).packedboard=packedboard;
  (*linkedlistpointer).movestosolution=0;
  (*linkedlistpointer).moves=NULL;  /* not necessary! */
  linkedlistpointer++;
  if((linkedlistpointer-linkedlist)>=LINKEDLISTSIZE){
    return NULL;
  }
  return l;
}





/* counts valid boards which are assumed to have been setup, up to
   rowcolnr-1  returns -1 if linkedlist is full
*/


int searchspace(int rowcolnr){
  int i,s,c;
  int count=0;
  struct linkedlistboardentry * l;
  packedboardtype packedboard;
  if(rowcolnr<=5){
    for(
	i=typedatas[striptypes[rowcolnr]].start;
	i<=typedatas[striptypes[rowcolnr]].end;
	i++){
      unpackedboard.strips[rowcolnr]=i;
      s=searchspace(rowcolnr+1);
      if(s!=-1){
	count+=s;
      }else{
	return -1;
      }
    }
    return count;
  }else if(rowcolnr<=11){
    for(
	i=typedatas[striptypes[rowcolnr]].start;
	i<=typedatas[striptypes[rowcolnr]].end;
	i++){
#ifdef FAST
      c=testcompatibilitycolumnfast(rowcolnr-6, i);
#else
      c=testcompatibilitycolumn(rowcolnr-6, i);
#endif
      if(c){
	unpackedboard.strips[rowcolnr]=i;
	s=searchspace(rowcolnr+1);
	if(s!=-1){
	  count+=s;
	}else{
	  return -1;
	}
      }
     }
     return count;
  }else{
    packedboard=packboard();
    l=insertinlinkedlist(packedboard);
    if(l==NULL){return -1;}
    if(!equal((*l).packedboard,packedboard)){
      fprintf(stderr,"Error in insertinlinkedlist\n");
      dumpstrips(stderr);
      exit(-1);
    }
	
    if(insertinhashtable(packedboard,l)==-1){
      return -1;
    }
    return 1;
  }
}


void inithashtable(){
  struct linkedlistboardentry ** p;
  struct linkedlistboardentry ** endofhashtable;
  endofhashtable=hashtable+HASHTABLESIZE;
  for(p=hashtable;p<endofhashtable;p++){
    (*p)=NULL;
  }
}


void initlinkedlist(){
  linkedlistpointer=linkedlist;
  /* For backwards compatibility we put this here. It should go in a 
     separate initializer */
  movelistpointer=movelist;
}








struct linkedlistboardentry *lookupinhashtable(packedboardtype packedboard){
  int hashed;
  int originalhash;
  packedboardtype packedboard1;
  struct linkedlistboardentry *l;
  hashed=hash(packedboard);
  originalhash=hashed;
  while(TRUE){
    l=hashtable[hashed];
    packedboard1=(*l).packedboard;
    if(equal(packedboard,packedboard1)){
      return l;
    }else{
      hashed++;
      if(hashed==HASHTABLESIZE){
	hashed=0;
      }
      if(hashed==originalhash){
	fprintf(stderr,"trying to lookup non existant board");
	dumpstrips(stderr);
	  exit(-1);
      }
    }

  }

}





  
struct linkedlistboardentry * computemovestosolution(){
  struct linkedlistboardentry * l;
  struct linkedlistboardentry * mostcomplicatedlevel;
  struct linkedlistboardentry ** p;
  int changed;
  int depth=0;
  int resultofmove;
  int movefound;

  mostcomplicatedlevel=NULL;
  changed=TRUE;
  while(changed){
    depth++;
    changed=FALSE;
    for(l=linkedlist;
	l<endofboards;
	l++){
      if((*l).movestosolution==0){
	/* try moves */
	p=(*l).moves;
	movefound=FALSE;
	if((p!=NULL)&&!movefound){
	  while((*p)!=NULL){
	    resultofmove=(**p).movestosolution;
	    if((resultofmove!=0)&&(resultofmove!=depth+1)){
	      if(resultofmove!=depth){
		fprintf(stderr,"Problem\n");
		dumpstrips(stderr);
		exit(-1);
	      }
	      (*l).movestosolution=resultofmove+1;
	      if(!changed){
		mostcomplicatedlevel=l;
	      }
	      changed=TRUE;
	      movefound=TRUE;
	    }
	    p++;
	  }
	}
      }
    }
  }
  return mostcomplicatedlevel;
}

#ifdef FAST
packedboardtype insertmove(packedboardtype packedboard, 
			   int rowcol, 
			   int stripnr){
  int shift;
  if(rowcol<=5){
    shift=4*rowcol;
    packedboard.rows=(packedboard.rows & ~(0xF<<shift))+(stripnr<<shift);
  }else{
    shift=4*(rowcol-6);
    packedboard.columns=(packedboard.columns & ~(0xF<<shift))+(stripnr<<shift);
  }
  return packedboard;
}

#endif 




/* fills linked list with moves, returns size of linked list. -1 if full */
int computemoves()
{
  struct linkedlistboardentry  *ll;
  struct linkedlistboardentry **m;
  int j,k,move,b;
  int originalstrip;
  packedboardtype packedboard4;
  /* put in stopper */
  endofboards=linkedlistpointer;

  m=movelistpointer;
  for(ll=linkedlist;ll<endofboards;ll++){
    unpackboard((*ll).packedboard);
    if(unpackedboard.strips[2]==5){
	(*ll).movestosolution=1;
	(*ll).moves=NULL;
    }else{
      (*ll).moves=m;
      for(j=0;j<=11;j++){
	originalstrip=unpackedboard.strips[j];
	for(k=0;k<=3;k++){
	  move=strips[originalstrip].moves[k];
	  if(move!=0){
#ifdef FAST
	    b=testcompatibilityrowcolmovefast((*ll).packedboard,j, move);
#else
	    b=testcompatibilityrowcolmove(j, move);
#endif
	    /* debug
	    b1=testcompatibilityrowcolmove(j, move);
	    if(b!=b1){
	      printf("Problem strip=%d move=%d fast=%d slow=%d\n",j,move,b,b1);
		tophysicalboard();
		printphysicalboard();
	      }
	    debug */
	    if(b){

#ifdef FAST
      packedboard4=insertmove((*ll).packedboard,j,move);
#else

	      unpackedboard.strips[j]=move;
	      packedboard4=packboard();
	      unpackedboard.strips[j]=originalstrip;
#endif


	      *m=lookupinhashtable(packedboard4);
	      m++;
	      if((m-movelist)>=MOVELISTSIZE){
		return -1;
	      }
	    }
	  }
	}
      }
      *m=NULL;
      m++;
      if((m-movelist)>=MOVELISTSIZE){
	return -1;
      }
    
    }
  }
  return (m-movelist);
}





/* assumes that computemovestosolution has been computed */
/* not used */
/*
packedboardtype mostcomplicatedlevel(){
  int maximum=0;
  struct linkedlistboardentry * l;
  packedboardtype packedboard={0,0};
  for(l=linkedlist;
      l<endofboards;
      l++){
    if ((*l).movestosolution>maximum){
      maximum=(*l).movestosolution;
      packedboard=(*l).packedboard;
    }
  }
  return packedboard;
}
*/


/* assumes that computemovestosolution has been computed */
/* not used */
/*
int movestosolution(packedboardtype packedboard){
  return (*lookupinhashtable(packedboard)).movestosolution;
}
*/
void randomtypes(){
  int i;
  for(i=0;i<=11;i++){
    striptypes[i]=floor((rand()*4.0/(RAND_MAX+1.0)));
  }
  striptypes[2]=1;
}








































