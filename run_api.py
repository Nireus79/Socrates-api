#!/usr/bin/env python
"""
Run Socrates API with proper environment setup.
"""
import sys
import os

# Change to API directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Now import and run
from socrates_api.main import app, run

if __name__ == '__main__':
    run()
