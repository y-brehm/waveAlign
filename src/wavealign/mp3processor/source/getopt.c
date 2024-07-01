#include <stdio.h>
#include <string.h>

#include <getopt.h>

int opterr = 1;    /* if error message should be printed */
int optind = 1;    /* index into parent argv vector */
int optopt;        /* character checked for validity */
char *optarg;      /* argument associated with option */

static char *optcursor = NULL; /* cursor into current option */

int getopt(int argc, char * const argv[], const char *optstring)
{
    optarg = NULL;

    if (optcursor == NULL || *optcursor == '\0')
    {
        if (optind >= argc || argv[optind][0] != '-' || argv[optind][1] == '\0')
        {
            return -1;
        }
        if (strcmp(argv[optind], "--") == 0)
        {
            optind++;
            return -1;
        }
        optcursor = argv[optind] + 1;
        optind++;
    }

    optopt = *optcursor++;
    const char *optdecl = strchr(optstring, optopt);
    if (optdecl == NULL || optopt == ':')
    {
        if (opterr)
        {
            fprintf(stderr, "Unknown option '-%c'\n", optopt);
        }
        return '?';
    }
    if (optdecl[1] == ':')
    {
        if (*optcursor != '\0')
        {
            optarg = optcursor;
            optcursor = NULL;
        } else if (optind < argc)
        {
            optarg = argv[optind];
            optind++;
        } else
        {
            if (opterr)
            {
                fprintf(stderr, "Option '-%c' requires an argument\n", optopt);
            }
            return optstring[0] == ':' ? ':' : '?';
        }
    }
    return optopt;
}
