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

int testcompatibilityforprecompute1(int row3stripnr,
				    int row2stripnr,
				    int row1stripnr,
				    int columnstripnr,
				    int columnindex){
  unpackedboard.strips[0]=row1stripnr;
  unpackedboard.strips[1]=row2stripnr;
  unpackedboard.strips[2]=row3stripnr;
  unpackedboard.strips[3]=0;
  unpackedboard.strips[4]=0;
  unpackedboard.strips[5]=0;
  return testcompatibilitycolumn(columnindex, columnstripnr);
}

void precomputecolumninsert1(){
  int i,j,k,l,c;
  int partial=0;
  for(i=0;i<=15;i++){
    partial=(partial<<4)+i;
    for(j=0;j<=15;j++){
      partial=(partial<<4)+j;
      for(k=0;k<=15;k++){
	partial=(partial<<4)+k;
	for(l=0;l<=15;l++){
	  partial=(partial<<4)+l;
	  for(c=0;c<=5;c++){
	    partial=(partial<<3)+c;
	    columninsert1[partial]=(unsigned char) testcompatibilityforprecompute1( i,j,k,l,c);
	    partial>>=3;
	  }
	  partial>>=4;
	}
	partial>>=4;
      }
      partial>>=4;
    }
    partial>>=4;
  }
}

int testcompatibilityforprecompute2(int row6stripnr, 
				    int row5stripnr, 
				    int row4stripnr,
				    int columnstripnr,
				    int columnindex){
  unpackedboard.strips[0]=0;
  unpackedboard.strips[1]=0;
  unpackedboard.strips[2]=0;
  unpackedboard.strips[3]=row4stripnr;
  unpackedboard.strips[4]=row5stripnr;
  unpackedboard.strips[5]=row6stripnr;
  return testcompatibilitycolumn(columnindex, columnstripnr);
}

void precomputecolumninsert2(){
  int i,j,k,l,c;
  int partial=0;
  for(i=0;i<=15;i++){
    partial=(partial<<4)+i;
    for(j=0;j<=15;j++){
      partial=(partial<<4)+j;
      for(k=0;k<=15;k++){
	partial=(partial<<4)+k;
	for(l=0;l<=15;l++){
	  partial=(partial<<4)+l;
	  for(c=0;c<=5;c++){
	    partial=(partial<<3)+c;
	    columninsert2[partial]=(unsigned char) testcompatibilityforprecompute2( i,j,k,l,c);
	    partial>>=3;
	  }
	  partial>>=4;
	}
	partial>>=4;
      }
      partial>>=4;
    }
    partial>>=4;
  }
}


void precompute(){
  precomputecolumninsert1();
  precomputecolumninsert2();
}






