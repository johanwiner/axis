CC      = gcc
CFLAGS  = -g
RM      = rm -f


default: all

all: Hello

Hello: HelloWorld.c
ifeq ($(WITHIOBOX), yes)
	$(CC) $(CFLAGS) -o Hello HelloWorld.c
endif

clean veryclean:
	$(RM) Hello

