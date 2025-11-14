#!/usr/bin/env python3
# George Prielipp (265112)
# mod.py

# open the files
numbers = open('numbers.txt', 'r')
fds = [open('mod0.txt', 'w'), open('mod1.txt', 'w'), open('mod2.txt', 'w')]

# do the work
# the number % 3 = which file to write that number to
for line in numbers.readlines():
    num = int(line)
    fds[num % 3].write(f'{num}\n')

#close the files
numbers.close()
for fd in fds:
    fd.close()

