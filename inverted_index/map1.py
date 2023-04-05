#!/usr/bin/env python3
"""Map 1."""

import sys
import csv
import re

# MAP AND REDUCE 1 CLEAN INPUT.
for line in csv.reader(sys.stdin):
    # Clean input
    id, title, content = line
    text = title + " " + content  # Cat title and content 
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)  # Remove special chars
    text = text.casefold()  # all lowercase
    text_list = text.split()  # Should be delimited by space by default
    # Clean out stopwords
    with open('stopwords.txt') as stopwords:
        for word in stopwords:
            if word.strip() in text_list:
                text_list.remove(word.strip())
    string = ' '.join(text_list)
    print(f'{id}\t{string}')
