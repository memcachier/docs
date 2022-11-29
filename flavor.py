#!/usr/bin/env python

import re
import sys

if len(sys.argv) < 4:
    print("Usage: flavor.py in.md out.md var")

start = re.compile("^\*\*IF\((.+)\)\*\*.*")  # e.g. **IF(heroku)**
end =  "**ENDIF**"
ignore_line = False

var = sys.argv[3]  # e.g., "direct" or "heroku"

with open(sys.argv[1]) as f:
    with open(sys.argv[2], 'w') as out:
        for l in f:
            # find start
            m = start.match(l.strip())
            if m:
                if m.group(1) != var:
                    ignore_line = True
                else:
                    # we are ignoring
                    pass
            elif l.startswith(end):
                ignore_line = False
            elif not ignore_line:
                out.write(l)
            else:
                # we are ignoring
                pass
