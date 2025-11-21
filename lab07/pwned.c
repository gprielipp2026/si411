#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void pwned(){
	printf("You PWNed it!\n");
}

void foo(char * s){
	char q[40];
	strcpy(q,s);
}

int main(int argc, char *argv[]){
	if(argc < 2) {
		printf("Usage: %s \n", argv[0]);
	}
	else {
		foo(argv[1]);
	}
}
