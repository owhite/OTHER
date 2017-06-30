#!/usr/bin/env python

import re

with open('scrap.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')


rs = re.findall('[0-9][0-9][0-9][0-9]*',data)

for word in rs:
    if (len(word) > 6):
        print word
