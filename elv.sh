#!/bin/bash
# E.L.V ROOT ENGINE v1.0.0 ULTIMATE - Bash Wrapper
# Author: HxN (NONAME-ELV)

print_gradient_banner() {
    python3 -c '
import sys
text = "E̸L̸V̶ ̶R̷O̷O̵T̴ ̸E̴N̸G̶I̴N̵E̷ ̴v̵3̵.̵8̵.̵1̵ ̵U̵L̵T̵I̵M̵A̵T̵E̵"
r1, g1, b1 = 255, 0, 127
r2, g2, b2 = 0, 245, 212
chars = list(text)
total = len(chars)
if total > 0:
    for i, c in enumerate(chars):
        r = int(r1 + (r2 - r1) * i / max(total - 1, 1))
        g = int(g1 + (g2 - g1) * i / max(total - 1, 1))
        b = int(b1 + (b2 - b1) * i / max(total - 1, 1))
        sys.stdout.write(f"\033[38;2;{r};{g};{b}m{c}")
print("\033[0m")'
}

# Verifikasi ketersediaan python3 di environment
if ! command -v python3 &> /dev/null; then
    echo -e "\033[91m[!] Critical Error: python3 interpreter not found in environment path.\033[0m"
    exit 1
fi

# Render banner via wrapper
print_gradient_banner

# Eksekusi core engine python dengan melemparkan seluruh argumen
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/elv.py" "$@"
