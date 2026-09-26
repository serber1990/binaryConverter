#!/usr/bin/env python3
# This file is kept for backward compatibility.
# The main implementation is now in numbase.py at the repo root.
# Install via pip: pip install numbase-converter
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from numbase import main

if __name__ == '__main__':
    main()
