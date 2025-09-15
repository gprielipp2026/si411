ifndef NTHREADS
	NTHREADS=1
endif

ifndef HEAD
	cmd = prime
else
	cmd = prime | head -$(HEAD)
endif

SRCS = prime1.c prime2.c prime3.c
BINS = $(SRCS:%.c=%)

all: $(BINS)

%: %.c
	clang -o $@ $< -Wall -DNTHREADS=$(NTHREADS)
	#./$(cmd)

