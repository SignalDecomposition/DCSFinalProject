#ifndef _app_H_
#define _app_H_


enum FSMstate{state0,state1,state2,state3,state4,state5,state6,state7}; // global variable
enum SYSmode{mode0,mode1,mode2,mode3,mode4}; // global variable

struct FileSystem{
    unsigned int  FilesCount;
    char *FilesNames[3];
    int *FilesStart[3];
    int  FilesSizes[3];
};

#define infomation_seg_A 0x1000
#endif







