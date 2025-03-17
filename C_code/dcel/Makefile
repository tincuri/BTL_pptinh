dcel: main.o make_dcel.o dcel.o scan.o misc.o
	gcc -Wall -Wextra -o dcel -lm main.o make_dcel.o dcel.o scan.o misc.o

test: make_dcel.c dcel.c scan.c misc.c
	gcc -o dcel make_dcel.c dcel.c scan.c misc.c

main.o: main.c dcel.h make_dcel.h misc.h
	gcc -c main.c

make_dcel.o: make_dcel.c make_dcel.h dcel.h misc.h scan.h
	gcc -c make_dcel.c

dcel.o: dcel.c dcel.h misc.h
	gcc -c dcel.c 

misc.o: misc.c misc.h dcel.h
	gcc -c misc.c

scan.o: scan.c dcel.h misc.h
	gcc -c scan.c

clean:
	rm -f main.o dcel.o make_dcel.o misc.o scan.o
