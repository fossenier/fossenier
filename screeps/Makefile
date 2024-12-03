CC = gcc
CFLAGS = -Wall -Wextra -Werror -Wconversion -Wsign-conversion -std=c99 -pedancit -O -g
CPPFLAGS = -I.
LDFLAGS = -lm

OBJS = linked_list.O

.PHONY: all clean

all: linked_list

linked_list: ${OBJS}
	${CC} ${CFLAGS} ${OBJS} -o linked_list

linked_list.o: linked_list.c node.h
	${CC} ${CPPFLAGS} ${CFLAGS} -c linked_list.c -o linked_list.o

clean:
	rm -f linked_list linked_list.o
	@echo "all cleaned up"