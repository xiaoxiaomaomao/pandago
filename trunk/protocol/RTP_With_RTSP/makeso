#----------------------------------------------------------
#	
#	COPYRIGHT 2007 (C) DVN (Holdings) Ltd (Hongkong)
#
#	AUTHOR:		wangry@dvnchina.com
#	PURPOSE:	beautiful commone makefile
#	CREATED:	2007-12-10
#
#	MODIFICATION HISTORY
#	Date        By     Details
#	----------  -----  -------
#
#----------------------------------------------------------

LIBS = -lpthread
INCS = 
LIBNAME = librtsp.so
CC = gcc
OBJS := $(filter-out main.o, $(patsubst %.c,%.o,$(wildcard *.c)))

.PHONY: all clean
%.o: %.c
	$(CC) $(CFLAGS) $(INCS) -c -o $@ $<
all : $(OBJS)
	$(CC) -shared -o $(LIBNAME) $(LIBS) $(OBJS) 

clean :
	rm -f *.o
	rm -f $(LIBNAME)
	rm -f $(EXENAME)

