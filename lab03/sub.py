#!/usr/bin/env python3
# George Prielipp (265112)
# sub.py

# I used regex101.com to test my regex

import re

# read the text file
letters = open('letters.txt', 'r')
strings = letters.readlines()
letters.close()

mids = open('mids.txt', 'w')

for string in strings:
    if re.search(r'([^M\n]*M[^I\n]*I[^D\n]*D[^S\n]*S)', string):
        string = string.replace('M', 'm').replace('I', 'i').replace('D', 'd').replace('S', 's')
        mids.write(string)

mids.close()
