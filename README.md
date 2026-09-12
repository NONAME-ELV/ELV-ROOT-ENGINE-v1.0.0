# 💀 E.L.V ROOT ENGINE v1.0.0
**Advanced Linux Privilege Escalation & Enumeration Suite**

[![Author](https://img.shields.io/badge/Author-HxN-red.svg)]()
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg)]()

</div>

---

### ⚡ Overview
**E.L.V ROOT ENGINE** adalah utilitas otomatisasi *post-exploitation* yang dirancang untuk melakukan *enumeration* secara mendalam dan memetakan vektor *privilege escalation* (LPE) pada sistem berbasis Linux. 

Script ini dikembangkan untuk kebutuhan *research red team* guna memvalidasi efektivitas biner SUID, kapabilitas (*capabilities*), *weak permissions*, hingga konfigurasi file sensitif agar menghasilkan analisis *true positive* yang presisi.

---

### 🚀 Features
* **Automated & Manual Enumeration**: Mode eksekusi ganda untuk audit cepat (`-a`) maupun analisis manual mendalam (`-m`).
* **SUID Mapping Engine**: Identifikasi biner SUID non-standar dan pemetaan eksploitasi berbasis GTFOBins (read, write, exec, limit).
* **Environment & Victim Profiling**: Ekstraksi detail kernel, distribusi, arsitektur, dan struktur UID/GID pengguna secara real-time.
* **Sensitive File Audit**: Deteksi konfigurasi rentan pada `/etc/passwd`, `/etc/shadow`, direktori `/root`, serta file konfigurasi web (`wp-config.php`, `redis.conf`, `apache2.conf`).
* **Capabilities & Writable Search**: Pemindaian file berkemampuan khusus (`getcap`) dan pencarian *world-writable files* milik root.

---

### 📦 Installation & Requirements

Pastikan script ini dijalankan di dalam *environment* POSIX-compliant (Linux native, VM, atau WSL). Jangan mengeksekusinya langsung melalui *Command Prompt* Windows standar untuk menghindari *environment mismatch* (`ModuleNotFoundError`).

```bash
# Clone repositori
git clone [https://github.com/NONAME-ELV/elv-root-engine.git](https://github.com/NONAME-ELV/elv-root-engine.git)
cd elv-root-engine-v1.0.0

# Berikan izin eksekusi pada wrapper shell
chmod +x elv.sh

# Install dependensi opsional (jika diperlukan)
pip3 install -r requirements.txt

💻 Usage Examples
Tampilkan banner dan menu bantuan:
python3 elv.py -h

Jalankan automated privilege escalation process secara menyeluruh:
python3 elv.py -a

Enumerasi spesifik (misal: SUID binaries & PHP config enumeration):
python3 elv.py -m -s -p

Matikan output warna terminal (nocolor mode):
python3 elv.py -a -n

🛡️ Disclaimer
Tool ini dibuat murni untuk keperluan authorized security research, audit sistem internal, dan pembelajaran ethical hacking. Penulis (HxN) tidak bertanggung jawab atas penyalahgunaan atau kerusakan yang ditimbulkan akibat penggunaan perangkat lunak ini di luar batas legalitas.
📄 License
Distributed under the GNU General Public License v3.0. See LICENSE for more information.

