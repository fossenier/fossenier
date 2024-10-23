CFLAGS = -Wall -Wextra -Werror -Wconversion -Wsign-conversion -std=c99 -pedantic
CC = gcc # Maybe g++

OBJS = test.o

.PHONY: all clean

all: test

test: ${OBJS}
	${CC} ${CFLAGS} ${OBJS} -o test

test.o: test.c
	${CC} ${CFLAGS} -c test.c

clean:
	rm -f *.o test
