%module _hint
%{
#include "gtlevel.h"
%}

extern void bestmove(int packedrows, int packedcolumns);
extern void init();
extern int getbestmoverows();
extern int getbestmovecolumns();
extern void findlevel(int start, int end);
extern int getbestyoucando();
extern int getpackedrows();
extern int getpackedcolumns();
