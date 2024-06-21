#include "cyclic_redundancy_check.h"

/*
Cyclic Redundancy Check (CRC) is a technique for detecting errors in digital data.
MP3s use this to ensure the integrity of the MP3 header.
This function calculates the CRC value for the header of an MP3 file and stores it, so that potential readers (like Rekordbox) can verify the integrity of the file.
*/


void cyclicRedundancyCheckWriteHeader(int headerlength, char *header)
{
    int cyclicRedundancyCheckValue = 0xffff;
    int i;

    cyclicRedundancyCheckValue = _update(((unsigned char*)header)[2], cyclicRedundancyCheckValue);
    cyclicRedundancyCheckValue = _update(((unsigned char*)header)[3], cyclicRedundancyCheckValue);

    for (i = 6; i < headerlength; i++)
    {
        cyclicRedundancyCheckValue = _update(((unsigned char*)header)[i], cyclicRedundancyCheckValue);
    }

    // stores crc value in header file
    header[4] = cyclicRedundancyCheckValue >> 8;
    header[5] = cyclicRedundancyCheckValue & 255;
}

int _update(int value, int cyclicRedundancyCheckValue)
{
    int i;
    value <<= 8;

    for (i = 0; i < 8; i++)
    {
        value <<= 1;
        cyclicRedundancyCheckValue <<= 1;

        if (((cyclicRedundancyCheckValue ^ value) & 0x10000))
            cyclicRedundancyCheckValue ^= CYCLICREDUNDANCYCHECK_16_POLYNOMIAL;
    }

    return cyclicRedundancyCheckValue;
}
