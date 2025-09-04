#!/usr/bin/env python3
"""
Test script for JioSaavn integration with spotDL.
"""

import sys
import os

# Add the project root to the path so we can import spotdl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spotdl.console.entry_point import console_entry_point

if __name__ == "__main__":
    console_entry_point()