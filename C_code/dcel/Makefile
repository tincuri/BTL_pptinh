dcel: main.c make_dcel.c dcel.c scan.c misc.c
	gcc -o dcel main.c make_dcel.c dcel.c scan.c misc.c

test: make_dcel.c dcel.c scan.c misc.c
	gcc -o dcel make_dcel.c dcel.c scan.c misc.c

main.o: main.c dcel.h 
	gcc -c main.c

dcel.o: dcel.c dcel.h
	gcc -c dcel.c 

misc.o: misc.c misc.h dcel.h
	gcc -c misc.c

make_dcel.o: make_dcel.c make_dcel.h dcel.h
	gcc -c make_dcel

clean:
	rm -f main.o dcel.o
