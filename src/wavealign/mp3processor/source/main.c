#include <fcntl.h>
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include "getopt.c"
#else
#include <unistd.h>
#endif

#include "cyclic_redundancy_check.h"
#include "file_operations.h"

#define HEADERSIZE 4
#define MMSYSERR_NOERROR 0
#define WAVERR_BADFORMAT 32
#define MP3GAIN_NOERROR MMSYSERR_NOERROR
#define WRITEBUFFERSIZE 100000
#define M3G_ERR_CANT_MODIFY_FILE -1
#define M3G_ERR_CANT_MAKE_TMP -2
#define M3G_ERR_NOT_ENOUGH_TMP_SPACE -3
#define M3G_ERR_RENAME_TMP -4
#define BUFFERSIZE 3000000

FILE *outf;
FILE *inf = NULL;

unsigned char *wrdpntr;
unsigned long bitidx;
int UsingTemp = 0;
long inbuffer;
unsigned long filepos;
unsigned long writebuffercnt;
typedef struct {
  unsigned long fileposition;
  unsigned char val[2];
} wbuffer;
unsigned char *curframe;
int NowWriting = 0;
int BadLayer = 0;
int LayerSet = 0;
int Reckless = 0;
int wrapGain = 0;
unsigned char buffer[BUFFERSIZE];
wbuffer writebuffer[WRITEBUFFERSIZE];
short int saveTime;
static const double bitrate[4][16] = {
    {1, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 1},
    {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},
    {1, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 1},
    {1, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 1}};
static const double frequency[4][4] = {
    {11.025, 12, 8, 1}, {1, 1, 1, 1}, {22.05, 24, 16, 1}, {44.1, 48, 32, 1}};
long arrbytesinframe[16];

#ifndef RG_ERROR_H
#define RG_ERROR_H

#include <string.h>

#ifdef WIN32
#include <Windows.h>
#include <io.h>
#include <mmsystem.h>
#include <sys/stat.h>
BOOL blnCancel;
#include <stdio.h>
#define MMSYSERR_NOERROR 0
#define MMSYSERR_ERROR 01
#define WAVERR_BADFORMAT 32
typedef unsigned int MMRESULT;
#endif

#define MP3GAIN_NOERROR MMSYSERR_NOERROR
#define MP3GAIN_UNSPECIFED_ERROR MMSYSERR_ERROR
#define MP3GAIN_FILEFORMAT_NOTSUPPORTED WAVERR_BADFORMAT
#define MP3GAIN_CANCELLED 2006

#endif

/* fill the mp3 buffer */
static unsigned long fillBuffer(long savelastbytes) {
  unsigned long i;
  unsigned long skip;
  unsigned long skipbuf;

  skip = 0;
  if (savelastbytes < 0) {
    skip = -savelastbytes;
    savelastbytes = 0;
  }

  if (UsingTemp && NowWriting) {
    if (fwrite(buffer, 1, inbuffer - savelastbytes, outf) !=
        (size_t)(inbuffer - savelastbytes))
      return 0;
  }

  if (savelastbytes != 0) /* save some of the bytes at the end of the buffer */
    memmove((void *)buffer, (const void *)(buffer + inbuffer - savelastbytes),
            savelastbytes);

  while (skip > 0) { /* skip some bytes from the input file */
    skipbuf = skip > BUFFERSIZE ? BUFFERSIZE : skip;

    i = (unsigned long)fread(buffer, 1, skipbuf, inf);
    if (i != skipbuf)
      return 0;

    if (UsingTemp && NowWriting) {
      if (fwrite(buffer, 1, skipbuf, outf) != skipbuf)
        return 0;
    }
    filepos += i;
    skip -= skipbuf;
  }
  i = (unsigned long)fread(buffer + savelastbytes, 1,
                           BUFFERSIZE - savelastbytes, inf);

  filepos = filepos + i;
  inbuffer = i + savelastbytes;
  return i;
}

/* instead of writing each byte change, I buffer them up */
static void flushWriteBuff() {
  unsigned long i;
  for (i = 0; i < writebuffercnt; i++) {
    fseek(inf, writebuffer[i].fileposition, SEEK_SET);
    fwrite(writebuffer[i].val, 1, 2, inf);
  }
  writebuffercnt = 0;
};

static void addWriteBuff(unsigned long pos, unsigned char *vals) {
  if (writebuffercnt >= WRITEBUFFERSIZE) {
    flushWriteBuff();
    fseek(inf, filepos, SEEK_SET);
  }
  writebuffer[writebuffercnt].fileposition = pos;
  writebuffer[writebuffercnt].val[0] = *vals;
  writebuffer[writebuffercnt].val[1] = vals[1];
  writebuffercnt++;
};

static void set8Bits(unsigned short val) {
  static const unsigned char maskLeft8bits[8] = {0x00, 0x80, 0xC0, 0xE0,
                                                 0xF0, 0xF8, 0xFC, 0xFE};

  static const unsigned char maskRight8bits[8] = {0xFF, 0x7F, 0x3F, 0x1F,
                                                  0x0F, 0x07, 0x03, 0x01};
  val <<= (8 - bitidx);
  wrdpntr[0] &= maskLeft8bits[bitidx];
  wrdpntr[0] |= (val >> 8);
  wrdpntr[1] &= maskRight8bits[bitidx];
  wrdpntr[1] |= (val & 0xFF);

  if (!UsingTemp)
    addWriteBuff(filepos - (inbuffer - (wrdpntr - buffer)), wrdpntr);
}

static void skipBits(int nbits) {

  bitidx += nbits;
  wrdpntr += (bitidx >> 3);
  bitidx &= 7;

  return;
}

static unsigned char peek8Bits() {
  unsigned short rval;

  rval = wrdpntr[0];
  rval <<= 8;
  rval |= wrdpntr[1];
  rval >>= (8 - bitidx);

  return (rval & 0xFF);
}

static unsigned long skipID3v2() {
  /*
   *  An ID3v2 tag can be detected with the following pattern:
   *    $49 44 33 yy yy xx zz zz zz zz
   *  Where yy is less than $FF, xx is the 'flags' byte and zz is less than
   *  $80.
   */
  unsigned long ok;
  unsigned long ID3Size;

  ok = 1;

  if (wrdpntr[0] == 'I' && wrdpntr[1] == 'D' && wrdpntr[2] == '3' &&
      wrdpntr[3] < 0xFF && wrdpntr[4] < 0xFF) {

    ID3Size = (long)(wrdpntr[9]) | ((long)(wrdpntr[8]) << 7) |
              ((long)(wrdpntr[7]) << 14) | ((long)(wrdpntr[6]) << 21);

    ID3Size += 10;

    wrdpntr = wrdpntr + ID3Size;

    if ((wrdpntr + HEADERSIZE - buffer) > inbuffer) {
      ok = fillBuffer(inbuffer - (wrdpntr - buffer));
      wrdpntr = buffer;
    }
  }

  return ok;
}

static unsigned long frameSearch(int startup) {
  unsigned long ok;
  int done;
  static int startfreq;
  static int startmpegver;
  long tempmpegver;
  double bitbase;
  int i;

  done = 0;
  ok = 1;

  if ((wrdpntr + HEADERSIZE - buffer) > inbuffer) {
    ok = fillBuffer(inbuffer - (wrdpntr - buffer));
    wrdpntr = buffer;
    if (!ok)
      done = 1;
  }

  while (!done) {

    done = 1;

    if ((wrdpntr[0] & 0xFF) != 0xFF)
      done = 0; /* first 8 bits must be '1' */
    else if ((wrdpntr[1] & 0xE0) != 0xE0)
      done = 0; /* next 3 bits are also '1' */
    else if ((wrdpntr[1] & 0x18) == 0x08)
      done = 0; /* invalid MPEG version */
    else if ((wrdpntr[2] & 0xF0) == 0xF0)
      done = 0; /* bad bitrate */
    else if ((wrdpntr[2] & 0xF0) == 0x00)
      done = 0; /* we'll just completely ignore "free format" bitrates */
    else if ((wrdpntr[2] & 0x0C) == 0x0C)
      done = 0;                             /* bad sample frequency */
    else if ((wrdpntr[1] & 0x06) != 0x02) { /* not Layer III */
      if (!LayerSet) {
        switch (wrdpntr[1] & 0x06) {
        case 0x06:
          BadLayer = !0;
          // fprintf(stderr, "MPEG Layer I file, not a layer III file\n");
          return 0;
        case 0x04:
          BadLayer = !0;
          // fprintf(stderr, "is an MPEG Layer II file, not a layer III
          // file\n");
          return 0;
        }
      }
      done = 0; /* probably just corrupt data, keep trying */
    } else if (startup) {
      startmpegver = wrdpntr[1] & 0x18;
      startfreq = wrdpntr[2] & 0x0C;
      tempmpegver = startmpegver >> 3;
      if (tempmpegver == 3)
        bitbase = 1152.0;
      else
        bitbase = 576.0;

      for (i = 0; i < 16; i++)
        arrbytesinframe[i] =
            (long)(floor(floor((bitbase * bitrate[tempmpegver][i]) /
                               frequency[tempmpegver][startfreq >> 2]) /
                         8.0));

    } else { /* !startup -- if MPEG version or frequency is different,
                            then probably not correctly synched yet */
      if ((wrdpntr[1] & 0x18) != startmpegver)
        done = 0;
      else if ((wrdpntr[2] & 0x0C) != startfreq)
        done = 0;
      else if ((wrdpntr[2] & 0xF0) == 0) /* bitrate is "free format" probably
                                            just corrupt data if we've already
                                            found valid frames */
        done = 0;
    }

    if (!done)
      wrdpntr++;

    if ((wrdpntr + HEADERSIZE - buffer) > inbuffer) {
      ok = fillBuffer(inbuffer - (wrdpntr - buffer));
      wrdpntr = buffer;
      if (!ok)
        done = 1;
    }
  }

  if (ok) {
    if (inbuffer - (wrdpntr - buffer) <
        (arrbytesinframe[(wrdpntr[2] >> 4) & 0x0F] +
         ((wrdpntr[2] >> 1) & 0x01))) {
      ok = fillBuffer(inbuffer - (wrdpntr - buffer));
      wrdpntr = buffer;
    }
    bitidx = 0;
    curframe = wrdpntr;
  }
  return ok;
}

int changeGain(char *filename, float leftgainchange, float rightgainchange) {
  unsigned long ok;
  int mode;
  int cyclicRedundancyCheckFlag;
  unsigned char *Xingcheck;
  unsigned long frame;
  int nchan;
  int ch;
  int gr;
  unsigned char gain;
  int bitridx;
  int freqidx;
  long bytesinframe;
  int sideinfo_len;
  int mpegver;
  long gFilesize = 0;
  char *outfilename;
  float gainchange[2];
  int singlechannel;
  long outlength, inlength; /* size checker when using Temp files */

  outfilename = NULL;
  frame = 0;
  BadLayer = 0;
  LayerSet = Reckless;

  NowWriting = !0;

  if ((leftgainchange == 0) && (rightgainchange == 0))
    return 0;

  // fprintf(stderr, "Changing gain of %s by %f dB\n", filename,
  // leftgainchange); fprintf(stderr, "Changing gain of %s by %f dB\n",
  // filename, rightgainchange);

  const float gainOffset = 0.71f;

  gainchange[0] = leftgainchange * gainOffset;
  gainchange[1] = rightgainchange * gainOffset;
  singlechannel = !(leftgainchange == rightgainchange);

  if (saveTime)
    fileTime(filename, storeTime);

  gFilesize = getSizeOfFile(filename);

  if (UsingTemp) {
    fflush(stderr);
    fflush(stdout);
    outlength = (long)strlen(filename);
    outfilename = (char *)malloc(outlength + 5);
    strcpy(outfilename, filename);
    if ((filename[outlength - 3] == 'T' || filename[outlength - 3] == 't') &&
        (filename[outlength - 2] == 'M' || filename[outlength - 2] == 'm') &&
        (filename[outlength - 1] == 'P' || filename[outlength - 1] == 'p')) {
      strcat(outfilename, ".TMP");
    } else {
      outfilename[outlength - 3] = 'T';
      outfilename[outlength - 2] = 'M';
      outfilename[outlength - 1] = 'P';
    }

    inf = fopen(filename, "r+b");

    if (inf != NULL) {
      outf = fopen(outfilename, "wb");

      if (outf == NULL) {
        fclose(inf);
        inf = NULL;
        // fprintf(stderr, "Can't open %s for temp writing\n", outfilename);
        return M3G_ERR_CANT_MAKE_TMP;
      }
    }
  } else {
    inf = fopen(filename, "r+b");
  }

  if (inf == NULL) {
    if (UsingTemp && (outf != NULL))
      fclose(outf);
    // fprintf(stderr, "Can't open %s for modifying\n", filename);
    return M3G_ERR_CANT_MODIFY_FILE;
  } else {
    writebuffercnt = 0;
    inbuffer = 0;
    filepos = 0;
    bitidx = 0;
    ok = fillBuffer(0);
    if (ok) {

      wrdpntr = buffer;

      ok = skipID3v2();

      ok = frameSearch(!0);
      if (!ok) {
        if (!BadLayer)
          printf("Can't find any valid MP3 frames in file %s\n", filename);
      } else {
        LayerSet = 1; /* We've found at least one valid layer 3 frame.
                       * Assume any later layer 1 or 2 frames are just
                       * bitstream corruption
                       */
        mode = (curframe[3] >> 6) & 3;

        if ((curframe[1] & 0x08) == 0x08) /* MPEG 1 */
          sideinfo_len = (mode == 3) ? 4 + 17 : 4 + 32;
        else /* MPEG 2 */
          sideinfo_len = (mode == 3) ? 4 + 9 : 4 + 17;

        if (!(curframe[1] & 0x01))
          sideinfo_len += 2;

        Xingcheck = curframe + sideinfo_len;

        // LAME CBR files have "Info" tags, not "Xing" tags
        if ((Xingcheck[0] == 'X' && Xingcheck[1] == 'i' &&
             Xingcheck[2] == 'n' && Xingcheck[3] == 'g') ||
            (Xingcheck[0] == 'I' && Xingcheck[1] == 'n' &&
             Xingcheck[2] == 'f' && Xingcheck[3] == 'o')) {
          bitridx = (curframe[2] >> 4) & 0x0F;
          if (bitridx == 0) {
            // fprintf(stderr, "is free format (not currently supported)\n");
            ok = 0;
          } else {
            mpegver = (curframe[1] >> 3) & 0x03;
            freqidx = (curframe[2] >> 2) & 0x03;

            bytesinframe =
                arrbytesinframe[bitridx] + ((curframe[2] >> 1) & 0x01);

            wrdpntr = curframe + bytesinframe;

            ok = frameSearch(0);
          }
        }

        frame = 1;
      } /* if (!ok) else */

#ifdef WIN32
      while (ok && (!blnCancel)) {
#else
      while (ok) {
#endif
        bitridx = (curframe[2] >> 4) & 0x0F;
        if (singlechannel) {
          if ((curframe[3] >> 6) &
              0x01) { /* if mode is NOT stereo or dual channel */
            // fprintf(stderr, "Can't adjust single channel for mono or joint
            // stereo\n");
            ok = 0;
          }
        }
        if (bitridx == 0) {
          // fprintf(stderr, "is free format (not currently supported)\n");
          ok = 0;
        }
        if (ok) {
          mpegver = (curframe[1] >> 3) & 0x03;
          cyclicRedundancyCheckFlag = curframe[1] & 0x01;
          freqidx = (curframe[2] >> 2) & 0x03;

          bytesinframe = arrbytesinframe[bitridx] + ((curframe[2] >> 1) & 0x01);
          mode = (curframe[3] >> 6) & 0x03;
          nchan = (mode == 3) ? 1 : 2;

          if (!cyclicRedundancyCheckFlag) /* we DO have a cyclicRedundancyCheck
                                             field */
            wrdpntr =
                curframe + 6; /* 4-byte header, 2-byte cyclicRedundancyCheck */
          else
            wrdpntr = curframe + 4; /* 4-byte header */

          bitidx = 0;

          if (mpegver == 3) { /* 9 bit main_data_begin */
            wrdpntr++;
            bitidx = 1;

            if (mode == 3)
              skipBits(5); /* private bits */
            else
              skipBits(3); /* private bits */

            skipBits(nchan * 4); /* scfsi[ch][band] */
            for (gr = 0; gr < 2; gr++)
              for (ch = 0; ch < nchan; ch++) {
                skipBits(21);
                gain = peek8Bits();
                if (wrapGain)
                  gain += (unsigned char)(gainchange[ch]);
                else {
                  if (gain != 0) {
                    float new_gain = (float)gain + gainchange[ch];
                    if ((int)(gain) + gainchange[ch] > 255)
                      gain = 255;
                    else if ((int)gain + gainchange[ch] < 0)
                      gain = 0;
                    else
                      gain += (unsigned char)(gainchange[ch]);
                  }
                }
                set8Bits(gain);
                skipBits(38);
              }
            if (!cyclicRedundancyCheckFlag) {
              if (nchan == 1)
                cyclicRedundancyCheckWriteHeader(23, (char *)curframe);
              else
                cyclicRedundancyCheckWriteHeader(38, (char *)curframe);
              /* WRITETOFILE */
              if (!UsingTemp)
                addWriteBuff(filepos - (inbuffer - (curframe + 4 - buffer)),
                             curframe + 4);
            }
          } else {     /* mpegver != 3 */
            wrdpntr++; /* 8 bit main_data_begin */

            if (mode == 3)
              skipBits(1);
            else
              skipBits(2);

            /* only one granule, so no loop */
            for (ch = 0; ch < nchan; ch++) {
              skipBits(21);
              gain = peek8Bits();
              if (wrapGain)
                gain += (unsigned char)(gainchange[ch]);
              else {
                if (gain != 0) {
                  if ((int)(gain) + gainchange[ch] > 255)
                    gain = 255;
                  else if ((int)gain + gainchange[ch] < 0)
                    gain = 0;
                  else
                    gain += (unsigned char)(gainchange[ch]);
                }
              }
              set8Bits(gain);
              skipBits(42);
            }
            if (!cyclicRedundancyCheckFlag) {
              if (nchan == 1)
                cyclicRedundancyCheckWriteHeader(15, (char *)curframe);
              else
                cyclicRedundancyCheckWriteHeader(23, (char *)curframe);
              /* WRITETOFILE */
              if (!UsingTemp)
                addWriteBuff(filepos - (inbuffer - (curframe + 4 - buffer)),
                             curframe + 4);
            }
          }
          wrdpntr = curframe + bytesinframe;
          ok = frameSearch(0);
        }
      }
    }

#ifdef WIN32
    if (blnCancel) { // need to clean up as best as possible
      fclose(inf);
      if (UsingTemp) {
        fclose(outf);
        deleteFile(outfilename);
        free(outfilename);
        // fprintf(stderr, "Cancelled processing\n");
      } else {
        // fprintf(stderr, "Cancelled processing.\n %s is probably corrupted
        // now.\n", filename);
      }
      if (saveTime)
        fileTime(filename, setStoredTime);
      return;
    }
#endif

    fflush(stderr);
    fflush(stdout);
    if (UsingTemp) {
      while (fillBuffer(0))
        ;
      fflush(outf);
#ifdef WIN32
      outlength = _filelength(_fileno(outf));
      inlength = _filelength(_fileno(inf));
#else
      fseek(outf, 0, SEEK_END);
      fseek(inf, 0, SEEK_END);
      outlength = ftell(outf);
      inlength = ftell(inf);
#endif
      fclose(outf);
      fclose(inf);
      inf = NULL;

      if (outlength != inlength) {
        deleteFile(outfilename);
        // fprintf(stderr, "Not enough temp space on disk to modify %s\n",
        // filename);
        return M3G_ERR_NOT_ENOUGH_TMP_SPACE;
      } else {

        if (deleteFile(filename)) {
          deleteFile(outfilename); // try to delete tmp file
                                   //
          // fprintf(stderr, "Can't open %s for writing\n", filename);
          return M3G_ERR_CANT_MODIFY_FILE;
        }
        if (moveFile(outfilename, filename)) {
          // fprintf(stderr, "Can't rename %s to %s\n", outfilename, filename);
          return M3G_ERR_RENAME_TMP;
        };
        if (saveTime)
          fileTime(filename, setStoredTime);
      }
      free(outfilename);
    } else {
      flushWriteBuff();
      fclose(inf);
      inf = NULL;
      if (saveTime)
        fileTime(filename, setStoredTime);
    }
  }

  NowWriting = 0;

  return 0;
}

int main(int argc, char *argv[]) {
  const char *usage = "Usage: %s -i filename -g gainChange\n";

  char *filename = NULL;
  float gainChange = 0.0f;

  int opt;
  while ((opt = getopt(argc, argv, "i:g:")) != -1) {
    switch (opt) {
    case 'i':
      filename = optarg;
      break;
    case 'g':
      gainChange = atof(optarg);
      break;
    default:
      // fprintf(stderr, usage, argv[0]);
      return 1;
    }
  }

  if (!filename || optind < argc) {
    // fprintf(stderr, usage, argv[0]);
    return 1;
  }

  float leftgainchange = gainChange;
  float rightgainchange = gainChange;

  int result = changeGain(filename, leftgainchange, rightgainchange);
  if (result != 0) {
    // fprintf(stderr, "Error: Could not change gain of file %s\n", filename);
    return 1;
  }

  printf("Successfully changed gain of file %s\n", filename);
  return 0;
}
