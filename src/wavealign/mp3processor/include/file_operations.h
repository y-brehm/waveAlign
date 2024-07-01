typedef enum {
    storeTime,
    setStoredTime
} timeAction;

long getSizeOfFile(char *filename);

int deleteFile(char *filename);

int moveFile(char *currentfilename, char *newfilename);

void fileTime(char *filename, timeAction action);
