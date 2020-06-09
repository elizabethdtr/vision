all: myClient

.PHONY: clean

myClient: myClient.c
	gcc -std=c99 myClient.c -o myClient -lopen62541
	@echo myClient is built - compilation successful

clean:
	rm -f myClient
