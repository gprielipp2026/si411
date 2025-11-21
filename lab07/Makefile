all:
	gcc bar.c -g -fno-stack-protector -o bar -m32 -mpreferred-stack-boundary=2
	gcc pwned.c -g -fno-stack-protector -o pwned -m32 -mpreferred-stack-boundary=2