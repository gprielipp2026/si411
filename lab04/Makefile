
SRCS=$(wildcard *.c)
TARGETS=$(SRCS:%.c=%)

all: $(TARGETS)

%: %.c
	clang $(CFLAGS) -o $@ $<
