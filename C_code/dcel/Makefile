dcel: main.o dcel.o
	gcc -o dcel main.o dcel.o

main.o: main.c dcel.h 
	gcc -c main.c

dcel.o: dcel.c dcel.h
	gcc -c dcel.c 

clean:
	rm -f main.o dcel.o
