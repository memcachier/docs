#!/usr/bin/env python3

import re
import sys

if len(sys.argv) < 2:
    print("Usage: check_links.py in.md")

rx_header = re.compile("^#+ (.+)$")
set_header = set()
rx_link = re.compile(".*]\(#(.+?)\).*")
set_link = set()

with open(sys.argv[1]) as f:
    for l in f:
        # get available header links
        hr = rx_header.match(l.strip())
        if hr:
            h = hr.group(1).lower()
            # NOTE: This is for GitHub.
            # h = re.sub("[\(\).:&]", "", h)
            # h = re.sub(" ", "-", h.strip())
            # NOTE: Heroku works slightly different. It seems to replace special
            # characters with a space and then squashes consecutive spaces
            # (just a guess).
            h = re.sub("[\(\).:&\+]", " ", h)
            h = re.sub("\s+", "-", h.strip())
            set_header.add(h)
        # get used references
        lr = rx_link.match(l)
        if lr:
            set_link.add(lr.group(1))

for l in set_link:
    if l not in set_header:
        print("Dangling link found: " + l)
