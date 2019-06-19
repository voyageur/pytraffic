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

char gtrafficboard[512]={'\0'};


struct gtrafficcar gtrafficstrips[16][2]=
{
  {{0,0},{0,0}},   /* 0 */
  {{0,2},{0,0}},   /* 1 */
  {{1,2},{0,0}},   /* 2 */
  {{2,2},{0,0}},   /* 3 */
  {{3,2},{0,0}},   /* 4 */
  {{4,2},{0,0}},   /* 5 */
  {{0,3},{0,0}},   /* 6 */
  {{1,3},{0,0}},   /* 7 */
  {{2,3},{0,0}},   /* 8 */
  {{3,3},{0,0}},   /* 9 */
  {{0,2},{2,2}},   /* 10 */
  {{0,2},{3,2}},   /* 11 */
  {{0,2},{4,2}},    /* 12 */
  {{1,2},{3,2}},     /* 13 */
  {{1,2},{4,2}},     /* 14 */
  {{2,2},{4,2}}      /* 15 */
};


char *colors[18]={
  "DarkGreen",
  "purple3",
  "orange",
  "seagreen",
  "blue3",
  "SteelBlue1",
  "yellow",
  "gold3",
   "IndianRed1",
    "SteelBlue4",
   "LightSkyBlue1",
   "SlateGray2",
   "LavenderBlush1",
   "LemonChiffon1",
    "MistyRose2",
    "NavajoWhite4"
   "thistle2",
};

/* computes a string for use with gtraffic */



void togtrafficboard(int m){
  
  int i,j;
  struct gtrafficcar g;
  char scratch[100];
  int colorindex=0;
  int stripnr;
  gtrafficboard[0]='\0';
  strcat(gtrafficboard,"1,"); /* one car must be removed */

  sprintf(scratch,"%d",m-1);
  strcat(gtrafficboard,scratch); /*moves to solution */
  strcat(gtrafficboard," "); 
  for(i=0;i<=11;i++){ 
    stripnr=unpackedboard.strips[i];
    for(j=0;j<=1;j++){
         g=gtrafficstrips[stripnr][j];
	 if(g.carlength!=0){
	   if(i<=5){   /* horizontal cars */
	     sprintf(scratch,"%d",g.carpos); 
	     strcat(gtrafficboard,scratch); /* xpos */
	     strcat(gtrafficboard,",");
	     sprintf(scratch,"%d",i); 
	     strcat(gtrafficboard,scratch);  /* ypos */
	     strcat(gtrafficboard,",1,");    /* horizontal */
	     if(i==2){
	       strcat(gtrafficboard,"1,");   /* red car */
	     }else{
	       strcat(gtrafficboard,"0,");
	     }
	   }else{
	     sprintf(scratch,"%d",i-6); 
	     strcat(gtrafficboard,scratch);  /* xpos */
	     sprintf(scratch,"%d",g.carpos); 
	     strcat(gtrafficboard,",");
	     strcat(gtrafficboard,scratch); /* ypos */
	     strcat(gtrafficboard,",0,");    /* vertical */
	     strcat(gtrafficboard,"0,");
	   }

	   sprintf(scratch,"%d",g.carlength); 
	   strcat(gtrafficboard,scratch); /* length */
  	   strcat(gtrafficboard,",");

	   if(i==2){
	     strcat(gtrafficboard,"red");   /* red car */
	   }else{
	     strcat(gtrafficboard,colors[colorindex++]);
	   }
	   strcat(gtrafficboard," ");
	 } 
       }
    }
}  

void creategtrafficdeck(int quantity, int treshold){
  int i;
  struct linkedlistboardentry * mostcomplicatedlevel;
  int requestedlevelfound;
  int m ;
  printf("[Intermediate]\n");
  fflush(stdout);
  for(i=1;i<=quantity;i++){
    requestedlevelfound=FALSE;
    while(!requestedlevelfound){
      randomtypes();
      mostcomplicatedlevel=doprep();
      if(mostcomplicatedlevel!=NULL){
	if((m=(*mostcomplicatedlevel).movestosolution)>treshold){
	  requestedlevelfound=TRUE;
	  unpackboard((*mostcomplicatedlevel).packedboard);
	  togtrafficboard(m);
	  printf("Card%d=%s\n",i,gtrafficboard);
	  fflush(stdout);
	}
      }
    }
  }
}



