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


void makestatistics(){
  FILE * fp;
  int i;
  int c;
  mostcomplexsolution=0;
  for(i=0;i<MAXMOVESTOSOLUTION;i++){
    statistics[i]=0;
  }
  if((fp=fopen("masterfile","r"))==NULL){
    fprintf(stderr,"masterfile does not exist\n");
    exit(-1);
  }
  while((c=getc(fp))!=EOF){
    if(c< MAXMOVESTOSOLUTION){
      statistics[c]++;
      if(c>mostcomplexsolution){
	mostcomplexsolution=c;
      }
    }else{
      fprintf(stderr,"masterfile corrupt\n");
      exit(-1);
    }
  }
  fclose(fp);
}

void makedirectory(){
  int lengthofdirectory;
  int cumul,i;

  /* the +2 comes from the fact that we also have a pointer 
     pointing just beyond the end of file.
  */  
  entriesindirectory=mostcomplexsolution-MINMOVESTOSOLUTION+2;
  /* the +2 comes from the fact that at offset 0 we have the
     least complicated and at offset 1 the most complicated solution
  */
    
  lengthofdirectory=(sizeof(int))*(entriesindirectory+2);
  cumul=0;
  directory[0]=MINMOVESTOSOLUTION;
  directory[1]=mostcomplexsolution;
  for(i=2;i<=entriesindirectory+1;i++){
    directory[i]=2*sizeof(int)*cumul+lengthofdirectory;
    cumul=statistics[i+MINMOVESTOSOLUTION-2]+cumul;
  }
}  

void writedirectory() {
  FILE * fp;
  fp=fopen("munch","w");
  fwrite(directory,sizeof(int),entriesindirectory+2,fp);
  fclose(fp);
}

void readdirectory(){
  FILE * fp;
  fp=fopen("../ttraffic.levels","r");
  fread(directory,sizeof(int),2,fp);
  if(directory[0]!=MINMOVESTOSOLUTION){
    fprintf(stderr,"error reading directory");
    exit(-1);
  }
  mostcomplexsolution=directory[1];
  entriesindirectory=mostcomplexsolution-MINMOVESTOSOLUTION+2;
  fread(directory+2,sizeof(int),entriesindirectory,fp);
  fclose(fp);
}

void makemunch () {
  int i,c;
  int packedstriptypes;
  FILE *masterfile, *munch;
  struct linkedlistboardentry * level;
  packedboardtype packedboard;

  makestatistics();
  makedirectory();
  writedirectory();
  munch=fopen("munch","a");
  for(i=MINMOVESTOSOLUTION; i<=mostcomplexsolution;i++){
    printf("Considering move %d\n",i);
    masterfile=fopen("masterfile","r");
    packedstriptypes=0;
    while((c=getc(masterfile))!=EOF){
      if(c==i){
	unpackstriptypes(packedstriptypes);
	level=doprep();
	packedboard=(*level).packedboard;
	fwrite(&(packedboard.rows),sizeof(int),1,munch);
	fwrite(&(packedboard.columns),sizeof(int),1,munch);
      }
      packedstriptypes++;
    }
    fclose(masterfile);
  }
  fclose(munch);
}

void testintegritymunch(){
  int lengthofdirectory, startoffset, endoffset;
  FILE *munch;
  packedboardtype packedboard;
  int i,j,h,sp,c;
  int spmax=0;
  int cmax=-1;
  struct linkedlistboardentry * l;
  readdirectory(); 
  munch=fopen("../ttraffic.levels","r");
  lengthofdirectory=(sizeof(int))*(entriesindirectory+2);
  printf("length of directory is %d\n",lengthofdirectory);
  fseek(munch,lengthofdirectory,SEEK_SET);
  for(i=MINMOVESTOSOLUTION; i<=mostcomplexsolution;i++){
    printf("Considering move %d\n",i);
    startoffset=directory[i+2-MINMOVESTOSOLUTION];
    endoffset=directory[i+3-MINMOVESTOSOLUTION];
    for(j=startoffset;j<endoffset;j+=2*sizeof(int)){
      printf("Considering board %d\n",j);
      fread(&(packedboard.rows),sizeof(int),1,munch);
      fread(&(packedboard.columns),sizeof(int),1,munch);
      unpackboard(packedboard);
      for(h=0;h<=11;h++){
	striptypes[h]= strips[unpackedboard.strips[h]].type;
      }
      inithashtable();
      initlinkedlist();
      sp=searchspace(0);
      c=-1;
      l=NULL;
      if(sp!=0 && sp!=-1){
	c=computemoves();
	if(c!=-1){
	  l= computemovestosolution();
	}
      }
      if(sp>spmax){
	spmax=sp;
      }
      if(c>cmax){
	cmax=c;
      }
      if(i!=l->movestosolution){
	fprintf(stderr, "munch corrupt\n");
	exit(-1);
      }else{
	printf ("searchspace=%d, moves=%d\n",spmax,cmax+1);
      }
    }
  }
}



