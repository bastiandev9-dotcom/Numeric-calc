================================================================
KALKULATOR METODE NUMERIK - ULTIMATE EDITION
Dengan Visualisasi Grafik, Export PNG/CSV/Excel/PDF/GIF,
Dark Mode, History, Validasi Real-time, Preset, Auto-Bracket,
Step-by-Step, Tooltip, Kalkulator Biasa, & Grafik Error
================================================================

Fitur Lengkap:
--------------
1.  Regula Falsi + Grafik Secant Line + Export PNG/CSV/PDF
2.  Newton-Raphson + Grafik Tangent Line (turunan otomatis) + Export PNG/CSV/PDF/GIF
3.  Iterasi Titik Tetap + Grafik Cobweb/Staircase + Export PNG/CSV/PDF/GIF
4.  Perbandingan 3 Metode Sekaligus + Grafik Error vs Iterasi
5.  Step-by-Step Mode (1 iterasi per klik untuk belajar)
6.  Keypad Ilmiah lengkap (sin, cos, log, sqrt, pi, e, pangkat)
7.  Kalkulator Cepat (evaluasi ekspresi matematika langsung)
8.  Dark Mode / Light Mode toggle
9.  Riwayat Perhitungan (History panel)
10. Validasi Input Real-time (hijau=valid, merah=invalid)
11. Preset Contoh Soal (dropdown pilih soal, auto-fill semua field)
12. Auto-Detect Bracket (cari interval [a,b] otomatis untuk RF)
13. Tooltip Help (hover mouse untuk penjelasan)
14. Export PDF Report lengkap (grafik + hasil + metadata)
15. Export GIF Animasi (visualisasi per iterasi jadi animasi)
16. Export CSV & Excel
17. Toolbar Matplotlib interaktif (Zoom, Pan, Reset di setiap grafik)

CARA INSTALL & JALAN:
---------------------
1. Pastikan Python 3.8+ sudah terinstall
   python --version

2. Install semua dependency:
   pip install -r requirements.txt

3. Jalankan aplikasi:
   python kalkulator_numerik_ultimate.py

DEPENDENCY:
-----------
- sympy       : perhitungan simbolik & turunan otomatis
- matplotlib  : visualisasi grafik
- numpy       : komputasi numerik
- pandas      : manipulasi data (export CSV/Excel)
- openpyxl    : export file Excel .xlsx
- Pillow      : manipulasi gambar (export GIF)
- reportlab   : export PDF laporan
- tkinter     : GUI (biasanya built-in)

JIKA ERROR TKINTER:
-------------------
Linux (Ubuntu/Debian):
   sudo apt-get install python3-tk

Linux (Fedora):
   sudo dnf install python3-tkinter

macOS (Homebrew Python):
   brew install python-tk

Windows:
   Tkinter biasanya sudah include. Jika tidak, reinstall Python 
   dan centang "tcl/tk and IDLE" saat instalasi.

CARA PENGGUNAAN:
----------------
1. Keypad Ilmiah (Panel Kiri):
   - Klik field input di tab mana pun
   - Tekan tombol keypad (angka/fungsi/operator)
   - Klik "Masukkan ke Field Aktif"

2. Setiap Tab Metode:
   - Pilih Preset Soal dari dropdown (auto-fill)
   - Atau isi manual. Field berubah hijau jika valid, merah jika invalid
   - Klik "HITUNG" untuk hasil + grafik
   - Klik "Auto Cari a,b" (khusus RF) untuk deteksi interval otomatis
   - Gunakan toolbar di bawah grafik untuk Zoom/Pan/Reset
   - Klik "Simpan Grafik" untuk export PNG (300 DPI)
   - Klik "CSV" untuk export data iterasi ke CSV/Excel
   - Klik "PDF" untuk export laporan lengkap
   - Klik "GIF" (NR & Iterasi) untuk export animasi

3. Tab Perbandingan:
   - Isi f(x), parameter, dan g(x)
   - Klik "BANDINGKAN 3 METODE"
   - Lihat ringkasan iterasi, grafik perbandingan akar, dan grafik error vs iterasi

4. Tab Step-by-Step:
   - Pilih metode dari dropdown
   - Klik "START" untuk inisialisasi
   - Klik "NEXT ITERASI" berulang untuk melihat perubahan per iterasi
   - Klik "RESET" untuk mengulang

5. Toolbar Atas:
   - "Dark/Light Mode" : Toggle tema gelap/terang
   - "History"         : Lihat riwayat semua perhitungan
   - "Bantuan"         : Panduan penggunaan

CONTOH SOAL:
------------
1. Akar x^2 - 5 = 0
   - RF: f(x)=x^2-5, a=1, b=3
   - NR: f(x)=x^2-5, x0=2
   - IT: g(x)=(x+5/x)/2, x0=2

2. Akar x^3 - x - 2 = 0
   - RF: f(x)=x^3-x-2, a=1, b=2
   - NR: f(x)=x^3-x-2, x0=2
   - IT: g(x)=(x+2)^(1/3), x0=2

3. sin(x) = x/2
   - RF: f(x)=sin(x)-x/2, a=1, b=3
   - NR: f(x)=sin(x)-x/2, x0=2
   - IT: g(x)=2*sin(x), x0=2

4. exp(x) = 3
   - RF: f(x)=exp(x)-3, a=0, b=2
   - NR: f(x)=exp(x)-3, x0=1
   - IT: g(x)=x-exp(x)+3+x, x0=1

TIPS:
-----
- Gunakan toolbar matplotlib (di bawah grafik) untuk:
  Zoom in/out, Pan/geser, Reset tampilan
- Jika metode tidak konvergen, coba ubah tebakan awal atau batas interval
- Untuk Iterasi, pastikan |g'(x)| < 1 di sekitar akar agar konvergen
- Grafik Error vs Iterasi di tab Perbandingan menunjukkan kecepatan konvergensi
- Mode Step-by-Step sangat cocok untuk belajar cara kerja tiap metode
