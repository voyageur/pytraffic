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


void dumpstrips(FILE * f){
  int i;
  for(i=0;i<=11;i++){
    fprintf(f,"%d",striptypes[i]);
  }
  fprintf(f,"\n");
}


void printhashtable(){
  int i;
  packedboardtype packedboard;
  struct linkedlistboardentry * l;
  printf("Dumping hashtable\n");
  for(i=0;i<HASHTABLESIZE;i++){
    l=hashtable[i];
    if(l!=NULL){
      packedboard=(*l).packedboard;
      printf("%x %x\n",packedboard.rows,packedboard.columns);
      unpackboard(packedboard);
      tophysicalboard();
      printphysicalboard();
      fflush(NULL);
    }
  }
}


void printlinkedlist(){
  struct linkedlistboardentry * l;
    printf("Dumping linkedlist\n");

  for(l=(struct linkedlistboardentry *)linkedlist;
      l<endofboards;
      l++){
    unpackboard((*l).packedboard);
    printf("%d%d\n",((*l).packedboard).rows,((*l).packedboard).columns);
    tophysicalboard();
    printphysicalboard();
    printf("moves to solution=%d\n",(*l).movestosolution);
    fflush(stdin);
  }
}

void printmoves(){
  struct linkedlistboardentry * l;
  struct linkedlistboardentry ** p;
  int count=0;
  printf("Dumping moves\n");

  for(l=linkedlist;
      l<endofboards;
      l++){
    printf("Board :\n");
    unpackboard((*l).packedboard);
    printf("%d%d\n",((*l).packedboard).rows,((*l).packedboard).columns);
    tophysicalboard();
    printphysicalboard();
    p=(*l).moves;
    if(p!=NULL){
      while((*p)!=NULL){
	printf("Move :\n");
	unpackboard((**p).packedboard);
	printf("%d%d\n",((**p).packedboard).rows,((**p).packedboard).columns);
	tophysicalboard();
	printphysicalboard();
	p++;
	count++;
      }
    }
  }
  printf("Number of moves=%d\n",count);
}

void randomboard(){
  int i;
  
  unpackedboard.strips[0]=floor((rand()*16.0/(RAND_MAX+1.0)));
  unpackedboard.strips[1]=floor((rand()*16.0/(RAND_MAX+1.0)));
  unpackedboard.strips[2]=typedatas[1].start+floor((rand()*5.0/(RAND_MAX+1.0)));
  unpackedboard.strips[3]=floor((rand()*16.0/(RAND_MAX+1.0)));
  unpackedboard.strips[4]=floor((rand()*16.0/(RAND_MAX+1.0)));
  unpackedboard.strips[5]=floor((rand()*16.0/(RAND_MAX+1.0)));
  unpackedboard.strips[6]=findcompatiblecolumn(0);
  unpackedboard.strips[7]=findcompatiblecolumn(1);
  unpackedboard.strips[8]=findcompatiblecolumn(2);
  unpackedboard.strips[9]=findcompatiblecolumn(3);
  unpackedboard.strips[10]=findcompatiblecolumn(4);
  unpackedboard.strips[11]=findcompatiblecolumn(5);
  for(i=0;i<=11;i++){
    striptypes[i]= strips[unpackedboard.strips[i]].type;
  }

}

double profile(int quantity){
  int i;
  int starttime,endtime;
  double average;
  starttime=time(NULL);
  for(i=1;i<=quantity;i++){
    randomtypes();
    doprep();
  }
  endtime=time(NULL);
  average=((endtime-starttime+0.0)/(quantity+0.0));
  return average;
}



void testtypes(){
   striptypes[0]=2;   
   striptypes[1]=1;   
   striptypes[2]=1;   
   striptypes[3]=1;   
   striptypes[4]=1;   
   striptypes[5]=3;   
   striptypes[6]=1;   
   striptypes[7]=1;   
   striptypes[8]=1;   
   striptypes[9]=1;   
   striptypes[10]=2;   
   striptypes[11]=1;
}

void printcolumninsert1(){
  int i, scratch, columnindex, columnstripnr;
  printf("Dumping columninsert1\n");
  for(i=0;i<COLUMNINSERTSIZE;i++){
    scratch=i;
    columnindex=scratch& 0x7;
    scratch>>=3;
    columnstripnr=scratch&0xF;
    scratch>>=4;
    unpackedboard.strips[2]=scratch & 0xF;
    scratch>>=4;
    unpackedboard.strips[1]=scratch & 0xF;
    scratch>>=4;
     unpackedboard.strips[0]=scratch & 0xF;
    scratch>>=4;
    unpackedboard.strips[5]=0;
    unpackedboard.strips[4]=0;
    unpackedboard.strips[3]=0;
    unpackedboard.strips[6]=0;
    unpackedboard.strips[7]=0;
    unpackedboard.strips[8]=0;
    unpackedboard.strips[9]=0;
    unpackedboard.strips[10]=0;
    unpackedboard.strips[11]=0;
    if(columnindex<=5){
      unpackedboard.strips[columnindex+6]=columnstripnr;
      tophysicalboard();
      printphysicalboard();
      printf("columninsert1=%d\n",columninsert1[i]);
      printf("%d,%d,%d,%d,%d\n",
	     unpackedboard.strips[0],
	     unpackedboard.strips[1],
	     unpackedboard.strips[2],
	     columnstripnr,
	     columnindex);
      printf("index=%x\n",i);
      printf("------------------\n------------------\n");
    }
  }
}

void printstatistics(){
  int i;
  printf("Printing statistics\n");
  printf("mostcomplexsolution=%d moves\n",
	mostcomplexsolution);
  for(i=0;i<=mostcomplexsolution;i++){
    printf("movestosolution=%3d, quantity=%8d\n",
	   i,statistics[i]);
  }
}

void printdirectory(void){
  int i;
  printf("Printing directory\n");
  printf("mostcomplexsolution=%d moves\n",
	mostcomplexsolution);
  printf("entries in directory=%d\n",entriesindirectory);
  for(i=0;i<=entriesindirectory-1;i++){
    printf("movestosolution=%3d, pointer=%8d\n",
	   i+MINMOVESTOSOLUTION,directory[i]);
  }
}

void showoffset (int offset){
  FILE * munch;
  int i;
  packedboardtype packedboard;
  munch=fopen("munch","r");
  fseek(munch,offset,SEEK_SET);
  fread(&(packedboard.rows),sizeof(int),1,munch);
  fread(&(packedboard.columns),sizeof(int),1,munch);
  unpackboard(packedboard);
  for(i=0;i<=11;i++){
    printf("%d=%d\n",i,unpackedboard.strips[i]);
  }
  tophysicalboard();
  printphysicalboard();
  togtrafficboard(0);
  printf("[Intermediate]\n");
  printf("Card1=%s\n",gtrafficboard);
}
