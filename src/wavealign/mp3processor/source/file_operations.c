#include <stdio.h>
#include <sys/stat.h>

#ifndef WIN32
#include <utime.h>
#else
#include <windows.h>
#endif


#include "file_operations.h"


long getSizeOfFile(char *filename)
{
    long size = 0;
    FILE *file;

    file = fopen(filename, "rb");
    if (file) {    
        fseek(file, 0, SEEK_END);
        size = ftell(file);
        fclose(file);
    }
  
    return size;
}

int deleteFile(char *filename)
{
    return remove(filename);
}

int moveFile(char *currentfilename, char *newfilename)
{
    return rename(currentfilename, newfilename);
}

void fileTime(char *filename, timeAction action)
{
	static        int  timeSaved=0;
#ifdef WIN32
	HANDLE outfh;
	static FILETIME create_time, access_time, write_time;
#else
    static struct stat savedAttributes;
#endif

    if (action == storeTime) {
#ifdef WIN32
		outfh = CreateFile((LPCTSTR)filename,
							GENERIC_READ,
							FILE_SHARE_READ,
							NULL,
							OPEN_EXISTING,
							FILE_ATTRIBUTE_NORMAL,
							NULL);
		if (outfh != INVALID_HANDLE_VALUE) {
			if (GetFileTime(outfh,&create_time,&access_time,&write_time))
				timeSaved = !0;

			CloseHandle(outfh);
		}
#else
        timeSaved = (stat(filename, &savedAttributes) == 0);
#endif
    }
    else {
        if (timeSaved) {
#ifdef WIN32
			outfh = CreateFile((LPCTSTR)filename,
						GENERIC_WRITE,
						0,
						NULL,
						OPEN_EXISTING,
						FILE_ATTRIBUTE_NORMAL,
						NULL);
			if (outfh != INVALID_HANDLE_VALUE) {
				SetFileTime(outfh,&create_time,&access_time,&write_time);
				CloseHandle(outfh);
			}
#else
			struct utimbuf setTime;	
			
			setTime.actime = savedAttributes.st_atime;
			setTime.modtime = savedAttributes.st_mtime;
			timeSaved = 0;

			utime(filename, &setTime);
#endif
		}
    }      
}
