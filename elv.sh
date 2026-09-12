#!/data/data/com.termux/files/usr/bin/bash
# E.L.V ROOT ENGINE v1.0.0 - Launcher

GREEN='\033[92m'
RED='\033[91m'
END='\033[0m'

cd "$(dirname "$0")"

if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo -e "${RED}[!] Python not found. Install: pkg install python${END}"
    exit 1
fi

if [ ! -f "elv.py" ]; then
    echo -e "${RED}[!] elv.py not found in this folder.${END}"
    exit 1
fi

echo -e "${GREEN}[+] Running E.L.V ROOT ENGINE...${END}"
"$PY" elv.py "$@"