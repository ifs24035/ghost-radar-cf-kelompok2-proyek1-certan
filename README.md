# 👻 Ghost Radar (Certainty Factor)

Game menebak lokasi hantu di papan 4×4 dengan petunjuk sensor yang kadang keliru.
Proyek mata kuliah **Kecerdasan Buatan**, Institut Teknologi Del.
Kategori algoritma: **Uncertainty**, memakai metode **Certainty Factor (CF)**.

## Ide Singkat

AI tidak tahu pasti di mana hantu bersembunyi. Setiap scan memberi petunjuk ("ada bisikan" atau "dingin")
yang bisa saja keliru. AI menyimpan skor CF untuk setiap petak yang belum dipilih, lalu memperbarui skor itu
setiap kali ada petunjuk baru. Petak dengan skor tinggi adalah petak yang paling mungkin menyimpan hantu.

## Fitur

- Papan **4×4**, satu level.
- Hantu **tidak bergerak** selama permainan.
- CF dihitung **hanya untuk petak yang belum dipilih**, sehingga petak di sekitar tebakan yang salah tidak jatuh ke 0.
- **Antarmuka klik** di notebook (ipywidgets): pilih aksi Scan atau Tangkap, lalu klik petak.
- **Saran scan AI** berbasis CF.
- **Mode dataset**: AI membaca riwayat scan dari file CSV.
- **Ekspor dataset**: menyimpan state CF tiap petak pada tiap langkah dari permainan yang dimainkan.
- **Versi web** (`index.html`) dengan logika yang sama.

## Aturan Permainan

- Hantu bersembunyi di satu petak. Pemain punya **3 nyawa** dan **8 baterai**.
- **Scan** (1 baterai): sensor memberi sinyal. Jika hantu dekat (di petak itu atau 8 petak di sekitarnya),
  sensor berbunyi dengan peluang 80%. Jika hantu jauh, sensor tetap berbunyi dengan peluang 15% (alarm palsu).
- **Tangkap**: jika benar, pemain menang. Jika salah, nyawa berkurang 1 dan petak itu terkunci (CF = 0).
- Scan tidak mengunci petak, jadi petak yang sama boleh di-scan ulang.
- Baris dan kolom dihitung mulai dari **0**.

## Cara Kerja Certainty Factor

Nilai awal setiap petak yang belum dipilih adalah **1 ÷ K** (K = jumlah petak yang belum dipilih).
Setiap scan menambah bukti ke setiap petak:

| Hasil sensor | Petak dekat (jarak ≤ 1) | Petak jauh |
|---|---|---|
| Ada bisikan | +0,60 | +0,08 |
| Dingin | +0,04 | +0,35 |

Dua nilai CF digabung dengan rumus:

```text
CF_baru = CF_lama + CF_bukti × (1 − CF_lama)
```

Contoh: dua bukti +0,60 menghasilkan 0,60 + 0,60 × (1 − 0,60) = **0,84**.

Catatan penting:
- Angka bukti ditetapkan oleh kelompok (penilaian pakar), bukan hasil hitungan.
- Skor CF **bukan peluang** dan tidak harus berjumlah 100%.
- AI dianggap **yakin** jika CF tertinggi ≥ 0,85 dan unggul ≥ 0,15 dari petak lain.
- Saran scan memakai heuristik: memilih petak yang membagi kandidat teratas secara seimbang.

## Dataset

- `scan_contoh.csv`: **masukan**, riwayat scan dengan kolom `baris, kolom, sinyal` (1 = ada bisikan, 0 = dingin).
- `dataset_state_grid_4x4.csv`: **hasil**, nilai CF setiap petak pada setiap langkah
  (kolom `Grid`, lalu `Langkah_0 (START)`, `Langkah_1 (SCAN ...)`, dan seterusnya). Direkam dari permainan nyata.

## Struktur Proyek

```text
ghost_radar.ipynb               notebook utama (AI, game, antarmuka klik, uji, simulasi)
scan_contoh.csv                 contoh dataset masukan
dataset_state_grid_4x4.csv      contoh dataset state per langkah
index.html                      versi web
app.py                          membuka index.html di browser
requirements.txt                daftar library
```

## Cara Menjalankan

### Notebook (VS Code)
1. Instal Python 3.10 atau lebih baru dan VS Code dengan ekstensi **Python** dan **Jupyter**.
2. Di folder proyek, buat dan aktifkan virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate.bat        # Windows cmd (PowerShell: .venv\Scripts\Activate.ps1)
   source .venv/bin/activate         # Mac / Linux
   ```
3. Instal library:
   ```bash
   pip install -r requirements.txt
   ```
4. Buka `ghost_radar.ipynb`, pilih kernel `.venv`, lalu jalankan cell dari atas ke bawah (Restart, lalu Run All).
5. Saat pertama kali memakai antarmuka klik, VS Code meminta izin mengunduh file pendukung widget.
   Klik **Enable Downloads** dan pastikan ada koneksi internet.

### Versi Web
Buka `index.html` dengan klik dua kali, atau jalankan:
```bash
python app.py
```
Atau lewat server lokal:
```bash
python -m http.server 8000
```
lalu buka `http://localhost:8000/index.html`.


## Keterbatasan

- CF di proyek ini berskala 0 sampai 1 dan hanya memuat bukti pendukung. Ini penyederhanaan dari CF pada MYCIN (−1 sampai +1).
- Skor CF cenderung naik mendekati 1 setelah beberapa scan, sehingga selisih antarpetak mengecil.
- Status "AI yakin" jarang tercapai sebelum baterai habis.
- Salah tangkap dicatat sebagai bukti "dingin" pada petak itu, yaitu keputusan desain kelompok.
- Saran scan kadang mengulang petak yang sama.
- Logika versi web dan notebook ditulis terpisah (JavaScript dan Python), jadi perubahan di salah satunya perlu disamakan manual.
