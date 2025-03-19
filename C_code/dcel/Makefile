CC=gcc

LIB= -L../seidel-1.0 -ltriangulate
dcel: main.o make_dcel.o dcel.o scan.o misc.o
	$(CC) -Wall -Wextra -o dcel -lm main.o make_dcel.o dcel.o scan.o misc.o $(LIB)

seid: main.o make_dcel.o dcel.o scan.o misc.o
	gcc -Wall -Wextra -o dcel -lm main.o make_dcel.o dcel.o scan.o misc.o ../seidel-1.0/tri.o ../seidel-1.0/misc.o ../seidel-1.0/construct.o ../seidel-1.0/monotone.o ../find_edge/find_edge.o

test: make_dcel.c dcel.c scan.c misc.c
	$(CC) -o dcel make_dcel.c dcel.c scan.c misc.c

main.o: main.c dcel.h make_dcel.h misc.h

make_dcel.o: make_dcel.c make_dcel.h dcel.h misc.h scan.h

dcel.o: dcel.c dcel.h misc.h

misc.o: misc.c misc.h dcel.h

scan.o: scan.c dcel.h misc.h

clean:
	rm -f main.o dcel.o make_dcel.o misc.o scan.o
