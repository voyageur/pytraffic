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

void unpackstriptypes(int packedstriptypes){
  striptypes[11]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[10]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[9]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[8]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[7]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[6]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[5]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[4]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[3]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[1]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[0]=packedstriptypes & 0x3;
  packedstriptypes>>=2;
  striptypes[2]=1;

}

void testintegrity(int start, int end){
  FILE * fp;
  int c,i;
  struct linkedlistboardentry * l;
  fp=fopen("masterfile","r");
  fseek(fp,start,SEEK_SET);
   for(i=start;i<end;i++){
     /*         printf("Checking i=%d\n",i); */
     unpackstriptypes(i);
     if((c=fgetc(fp))!=EOF){
       l=doprep();
       if(l==NULL){
	 if(c!=0){
	   dumpstrips(stderr);
	   fprintf(stderr,"masterfile corrupt\n");
	   exit(-1);
	 }
       }else{
	 if((*l).movestosolution!=c){
	   dumpstrips(stderr);
	   fprintf(stderr,"masterfile corrupt\n");
	   exit(-1);
	 } 
       }
     }else{
       break;
     }
   }
  fclose(fp);
}

int lengthofmasterfile(){
  struct stat buf;
  stat("masterfile",&buf);
  return buf.st_size;
}

void testintegritylast(int last){
  int filelength,start;
  filelength=lengthofmasterfile();
  start=filelength-last;
  if(start<0){start=0;}
  testintegrity(start,filelength);
}


void generatemasterfile(){
  struct linkedlistboardentry * l;
  FILE * fp;
  unsigned char  p;
  int filelength;
  int restarting=TRUE;
  testintegritylast(1024);
  filelength=lengthofmasterfile();
  fp=fopen("masterfile","a");
  for(striptypes[0]=0;striptypes[0]<4;striptypes[0]++){
  for(striptypes[1]=0;striptypes[1]<4;striptypes[1]++){
  for(striptypes[3]=0;striptypes[3]<4;striptypes[3]++){
  for(striptypes[4]=0;striptypes[4]<4;striptypes[4]++){
  for(striptypes[5]=0;striptypes[5]<4;striptypes[5]++){
  for(striptypes[6]=0;striptypes[6]<4;striptypes[6]++){
  for(striptypes[7]=0;striptypes[7]<4;striptypes[7]++){
  for(striptypes[8]=0;striptypes[8]<4;striptypes[8]++){
  for(striptypes[9]=0;striptypes[9]<4;striptypes[9]++){
  for(striptypes[10]=0;striptypes[10]<4;striptypes[10]++){
  for(striptypes[11]=0;striptypes[11]<4;striptypes[11]++){
    striptypes[2]=1;
    if(restarting){
      unpackstriptypes(filelength);
      restarting=FALSE;
    }
    l=doprep();
    if(l!=NULL){
      p=(*l).movestosolution;
    }else{
      p=0;
    }
    fwrite(&p,1,1,fp);
    /*    fflush(fp);*/
  }
  }
  }
  }
  }
  }
  }
  }
  }
  }
  }
  fclose(fp);
}


