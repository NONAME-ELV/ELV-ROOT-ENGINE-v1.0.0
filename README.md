# E.L.V ROOT ENGINE v1.0.0

**E.L.V ROOT ENGINE** is a Python-based `*nix` system enumeration and privilege-escalation assessment tool.

- **Author:** HxN
- **Version:** 1.0.0
- **License:** GNU GPL v3
- **Platform:** `*nix`

---

## Disclaimer

This tool is intended for **authorized security testing, security research, and educational purposes only**.

Only use E.L.V ROOT ENGINE on systems you own or have explicit permission to assess.

---

## Features

- Automated privilege-escalation assessment
- Manual system enumeration
- SUID binary enumeration
- Weak file-permission enumeration
- Weak ownership checks
- PHP configuration file enumeration
- Linux capabilities enumeration
- World-writable file enumeration
- Colorized terminal output
- Multiple enumeration categories

---

## Usage

```text
E.L.V ROOT ENGINE v1.0.0
[ Privilege Escalation Suite ]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show version and exit
  -a, --auto            automated privilege escalation process
  -m, --manual          system enumeration
  -n, --nocolor         disable color
  -b, --banner          show banner and exit
  -s, --suid            SUID binary enumeration
  -w, --weak            weak permissions of files enumeration
  -p, --php             PHP configuration files enumeration
  -c, --capabilities    capabilities enumeration
  -f, --full-writables  world writable files enumeration
```

### Basic Examples

```bash
./elv.sh -a
python3 elv.py -a
```

### Specific Categories

```bash
./elv.sh -a -s
python3 elv.py -m -w
```

Use the `-n` option with the above arguments to disable colored output.

---

## Installation & Setup

### Clone the Repository

```bash
git clone <your-repo-url>
cd ELVENGINE
```

---

## 1. `elv.sh` — Wrapper Execution

### Termux

```bash
pkg update && pkg upgrade
pkg install python coreutils zip

chmod +x elv.sh
./elv.sh -b
```

### Linux

```bash
sudo apt install python3

chmod +x elv.sh
./elv.sh -b
```

---

## 2. `elv.py` — Core Engine

The Python engine can also be executed directly without the wrapper script.

### Termux

```bash
pkg update && pkg upgrade
pkg install python coreutils zip

chmod +x elv.py
python3 elv.py -b
```

### Linux

```bash
sudo apt install python3

chmod +x elv.py
python3 elv.py -b
```

---

## Modes

### Manual

Manual mode performs system enumeration and assessment without automatically attempting privilege escalation.

```bash
./elv.sh -m
```

or:

```bash
python3 elv.py -m
```

### Auto

Auto mode performs automated privilege-escalation assessment based on the available enumeration results.

```bash
./elv.sh -a
```

or:

```bash
python3 elv.py -a
```

---

## Enumeration Categories

### SUID Binaries

- General SUID binaries
- SUID binaries relevant to file access
- SUID binaries relevant to file creation
- Limited SUID binaries
- Custom SUID checks

### Weak Permissions

Checks for potentially dangerous permissions involving:

- `/etc/passwd`
- `/etc/shadow`
- `apache2.conf`
- `httpd.conf`
- `redis.conf`
- `/root`

### Weak Ownership

Checks ownership of potentially sensitive files and directories, including:

- `/etc/passwd`
- `/etc/shadow`
- `apache2.conf`
- `httpd.conf`
- `redis.conf`
- `/root`

### Linux Capabilities

- General capabilities
- Custom capabilities
- Capabilities involving `CAP_SETUID`

### Interesting Files

- PHP configuration files
- World-writable files

---

## Command Examples

Display the banner:

```bash
./elv.sh -b
```

Display help:

```bash
./elv.sh -h
```

Run automated assessment:

```bash
./elv.sh -a
```

Run manual enumeration:

```bash
./elv.sh -m
```

Enumerate SUID binaries:

```bash
./elv.sh -m -s
```

Enumerate weak permissions:

```bash
./elv.sh -m -w
```

Disable colors:

```bash
./elv.sh -m -n
```

---

## Project Structure

```text
ELVENGINE/
├── elv.sh
├── elv.py
├── README.md
├── LICENSE
└── ...
```

---

## License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](LICENSE) for the full license text.

Copyright (C) 2026 HxN

---

## Contact

**Author:** HxN

**Project:** E.L.V ROOT ENGINE

---

> **E.L.V — Exploit Loader & Vulnerability Frimware**
