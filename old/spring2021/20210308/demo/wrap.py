#!/usr/bin/python3
import os
import sys
os.execve('./format', ['./format'] + sys.argv[2:], {})
