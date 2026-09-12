# E.L.V ROOT ENGINE v1.0.0

**E.L.V ROOT ENGINE** is a Python `*nix` Enumerator & Auto Privilege Escalation tool.

Author: **HxN**
License: **GNU GPL v3**
Version: **1.0.0**
Platform: **\*nix**

---

## Disclaimer

This tool is intended for **authorized security testing only**.

---

## Usage


E.L.V ROOT ENGINE v1.0.0
[ Privilege Escalation Suite ]
optional arguments:
-h, --help            show this help message and exit
-v, --version         show version and exit
-a, --auto            automated privilege escalation process
-m, --manual          system enumeration
-n, --nocolor         disable color
-b, --banner          show banner and exit
-s, --suid            suid binary enumeration
-w, --weak            weak permissions of files enumeration
-p, --php             PHP configuration files enumeration
-c, --capabilities    capabilities enumeration
-f, --full-writables  world writable files enumeration
usage examples:
./elv.sh -a
python3 elv.py -a
Specific categories usage examples:
./elv.sh -a -s
python3 elv.py -m -w
*Use the above arguments with -n to disable color.

---

## Installation & Setup

```bash
git clone <your-repo-url>
cd ELVENGINE

1. Script elv.sh (Wrapper Execution)
 * Termux:
   pkg update && pkg upgrade
pkg install python coreutils zip
chmod +x elv.sh
./elv.sh -b

 * Linux:
   sudo apt install python3
chmod +x elv.sh
./elv.sh -b

2. Script elv.py (Core Engine Direct Execution)
 * Termux:
   pkg update && pkg upgrade
pkg install python coreutils zip
chmod +x elv.py
python3 elv.py -b

 * Linux:
   sudo apt install python3
chmod +x elv.py
python3 elv.py -b

Modes
 * Manual — enumeration only, no auto-exploit
 * Auto — automated privilege escalation attempt
Exploitation Categories
SUID Binaries
 * General SUIDs
 * SUIDs for reading files
 * SUIDs for creating files as root
 * Limited SUIDs
 * Custom SUIDs
Weak Permissions
 * /etc/passwd
 * /etc/shadow
 * apache2.conf
 * httpd.conf
 * redis.conf
 * /root
Weak Ownership
 * /etc/passwd
 * /etc/shadow
 * apache2.conf
 * httpd.conf
 * redis.conf
 * /root
Capabilities
 * General capabilities
 * Custom capabilities
 * With CAP_SETUID
Interesting Files
 * PHP configuration files
 * World writable files
License
GNU General Public License v3.0. See LICENSE.
Copyright (C) 2026 HxN

Contact
 * Author: HxN
