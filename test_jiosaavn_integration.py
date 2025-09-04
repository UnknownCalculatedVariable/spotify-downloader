#!/usr/bin/env python3
"""
Test script to verify JioSaavn integration.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path so we can import spotdl
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import spotdl
        print("✓ spotdl imported successfully")
    except Exception as e:
        print(f"✗ Failed to import spotdl: {e}")
        return False
    
    try:
        from spotdl.console.jiosaavn_cmd import jiosaavn
        print("✓ jiosaavn command imported successfully")
    except Exception as e:
        print(f"✗ Failed to import jiosaavn command: {e}")
        return False
    
    try:
        from spotdl.console.jiosaavn.downloader import download_jiosaavn
        print("✓ jiosaavn downloader imported successfully")
    except Exception as e:
        print(f"✗ Failed to import jiosaavn downloader: {e}")
        return False
    
    try:
        from spotdl.download.downloader import Downloader
        print("✓ Downloader imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Downloader: {e}")
        return False
    
    return True

def test_help():
    """Test that the help command includes jiosaavn."""
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "spotdl", "--help"
        ], cwd=Path(__file__).parent, capture_output=True, text=True)
        
        if "jiosaavn" in result.stdout:
            print("✓ jiosaavn appears in help output")
            return True
        else:
            print("✗ jiosaavn does not appear in help output")
            return False
    except Exception as e:
        print(f"✗ Failed to test help output: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing JioSaavn integration...")
    print()
    
    tests = [
        test_imports,
        test_help,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! JioSaavn integration is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())