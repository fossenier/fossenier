# Logan Fossenier
# 11343891
# hzv143

CC = gcc
CFLAGS = -Werror -Wextra -Wsign-conversion -Wconversion -pedantic -g -std=c99
CPPFLAGS = -I.
# LDFLAGS = -L. -lnode

OBJS = linked_list

.PHONY: all clean

all: linked_list

linked_list.o: linked_list.c node.h
	${CC} ${CFLAGS} ${CPPFLAGS} -c linked_list.c -o linked_list.o

linked_list: linked_list.o node.h
	${CC} ${CFLAGS} ${CPPFLAGS} linked_list.o -o linked_list

clean:
	echo hi