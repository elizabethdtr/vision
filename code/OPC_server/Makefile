all: myServer serverVariables VariablesToProcesses myServerUpdated

.PHONY: clean

myServer: myServer.c
	gcc -std=c99 myServer.c -o myServer -lopen62541 
	@echo myServer is built - compilation successful
	
serverVariables: serverVariables.c
	gcc -std=c99 serverVariables.c -o serverVariables -lopen62541 
	@echo serverVariables is built - compilation successful
	
	
VariablesToProcesses: VariablesToProcesses.c
	gcc -std=c99 VariablesToProcesses.c -o VariablesToProcesses -lopen62541 
	@echo VariablesToProcesses is built - compilation successful

myServerUpdated: myServer_updated.c
	gcc -std=c99 myServer_updated.c -o myServerUpdated -lopen62541 
	@echo myServerUpdated is built - compilation successful

clean:
	rm -f myServer
	rm -f serverVariables
