#include "rtsp_util.h"
#include "stdlib.h"
#include "stdio.h"
#include "string.h"

char* rtsp_strdup(const char* str)
{
   
   int len = strlen(str);

   char *dest;

   if (len == 0)
   {
       return NULL;
   }

   dest = (char*) malloc(len + 1);
   strcpy(dest,str);
   return dest;
}
