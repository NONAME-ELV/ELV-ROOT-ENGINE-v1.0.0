#!/bin/bash
# E.L.V ROOT ENGINE v.1.0.0 ULTIMATE - Execution Wrapper
# Author: HxN (NONAME-ELV)
# Classification: Exploit Development

# --- 0X01. ENVIRONMENT SANITIZATION ---
if ! command -v python3 &> /dev/null; then
    echo -e "\033[91m[!] Critical Error: python3 interpreter not found in environment path.\033[0m"
    exit 1
fi

# --- 0X02. CORE ENGINE INTEGRITY CHECK ---
if [ ! -f "elv.py" ]; then
    echo -e "\033[91m[!] Critical Error: elv.py core engine not found in current directory.\033[0m"
    exit 1
fi

# --- 0X03. EXECUTION PIPELINE ---
# Meneruskan seluruh argumen (cth: -a, -s, dll) langsung ke core engine
python3 elv.py "$@"
