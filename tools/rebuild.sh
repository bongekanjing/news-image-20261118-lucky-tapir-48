#!/bin/sh
# Rebuild the page from the copy and check it, from inside tools/.
set -e
python3 compose.py ../entry.png
python3 check.py ../entry.png
