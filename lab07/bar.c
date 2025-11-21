
// to compile:
// gcc bar.c -g -fno-stack-protector -o bar -m32 -mpreferred-stack-boundary=2

#include <stdio.h>
#include <stdlib.h>

void bar(){
    char s[12]="AABBCCDDEEF";

    //<---- here

    return;
}



void foo(int a){
    int z=a + 3;
    bar();
    return;
}

int main(){
    int x=15;
    foo(x);
    exit(0);
}

