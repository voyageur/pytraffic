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

char physicalboard[6][6];


/* computes physicalboard from unpackedboard */
void tophysicalboard() 
{
  int i,j;
  int occupancyboard;
  int stripnr;
  char car;
  car='a';
  for(i=0;i<=5;i++){  /*printing horizontal strips*/
    stripnr=unpackedboard.strips[i];
    for(j=0;j<=5;j++){
      physicalboard[i][j]='.';
      occupancyboard=strips[stripnr].occupancy[j];
      if(occupancyboard!=0){
	physicalboard[i][j]=car+occupancyboard-1;
      }
    }
    car=car+typedatas[strips[stripnr].type].numberofstrips;
  }
  for(i=6;i<=11;i++){  /*printing vertical strips*/
    stripnr=unpackedboard.strips[i];
    for(j=0;j<=5;j++){
      occupancyboard=strips[stripnr].occupancy[j];
      if(occupancyboard!=0){
	physicalboard[j][i-6]=car+occupancyboard-1;
      }
    }
    car=car+typedatas[strips[stripnr].type].numberofstrips;
  }
}

void printphysicalboard(){
  int i,j;
  for(i=0;i<=5;i++){
    for(j=0;j<=5;j++){
      printf("%c",physicalboard[i][j]);
    }
    printf("\n");
  }
  printf("******\n");
}

void printsolution(){
  struct linkedlistboardentry * l;
  int i;
  for(i=0;i<MAXSOLUTION;i++){
    if((l=solution[i])!=NULL){
      printf("movestosolution=%d\n",(*l).movestosolution-1);
      unpackboard((*l).packedboard);
      tophysicalboard();
      printphysicalboard();
    }else{
      break;
    }
  }
}
