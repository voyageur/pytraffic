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
#include <getopt.h>

int optind;

enum actiontype{
DODECK,
PROFILE,
TEST,
MASTERFILE,
EXTRACT
};

int main(int argc,char* argv[])
{
  /*p=profile g=gtraffic q=quantity c=complexity 
    d=deterministic t=test m=masterfile e=extract*/
  char * opstring="pgqcdtme";
  char c;
  enum actiontype action=TEST;
  double average;
  int quantity=5;
  int complexity=5;
  int deterministic=FALSE;
#ifdef FAST
  precompute();
#endif
  while(!((c=getopt(argc,argv,opstring))==EOF)){
    switch (c){
    case 'g':
      action=DODECK;
      break;
    case 'q':
      quantity=atoi(argv[optind]);
      break;
    case 'c':
      complexity=atoi(argv[optind]);
      break;
    case 'd':
      deterministic=TRUE;
      break;
    case 'p':
      action=PROFILE;
      break;
    case 't':
      action=TEST;
      break;
    case 'm':
      action=MASTERFILE;
      break;
    case 'e':
      action=EXTRACT;
      break;
    default:
      /* do nothing */
      break;
    }
  }
  if(!deterministic){
    srand(time(NULL));
  }
  switch(action) {
  case DODECK:
     creategtrafficdeck(quantity,complexity); 
     break;
  case PROFILE:
    average=profile(quantity);
    printf("Average running time=%g\n",average);
    break;
  case TEST:
    testintegritymunch();
    break;
  case MASTERFILE:
    generatemasterfile();
    break;
  case EXTRACT:
    makemunch();
    break;
  default:
    /* impossible */
    break;
  }
  return 0;
}

