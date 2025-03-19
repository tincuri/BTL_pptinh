CC=gcc

LIB= -L../seidel-1.0 -ltriangulate
sleeve: main.o make_dcel.o dcel.o scan.o misc.o
	gcc -Wall -Wextra -lm main.o make_dcel.o dcel.o scan.o misc.o $(LIB) ../find_edge/find_edge.o  -o sleeve

sleeve_no_tri: main_no_tri.o make_dcel.o dcel.o scan.o misc.o
	$(CC) -Wall -Wextra -lm main_no_tri.o make_dcel.o dcel.o scan.o misc.o -o sleeve_no_tri

main.o: main.c dcel.h make_dcel.h misc.h

main_no_tri.o: main_no_tri.c dcel.h make_dcel.h misc.h

make_dcel.o: make_dcel.c make_dcel.h dcel.h misc.h scan.h

dcel.o: dcel.c dcel.h misc.h

misc.o: misc.c misc.h dcel.h

scan.o: scan.c dcel.h misc.h

clean:
	rm -f main.o dcel.o make_dcel.o misc.o scan.o main_no_tri.o
