# InSearch

InSearch adalah aplikasi demo yang dirancang untuk mengindeks dan mencari dokumen dalam folder yang ditentukan. Aplikasi ini mendukung pengindeksan file teks dan PDF, memungkinkan pengguna untuk mencari dokumen berdasarkan kata kunci.

## Fitur

- Mengindeks file teks dan PDF dalam folder yang ditentukan.
- Memperbarui indeks saat file ditambahkan, diubah, atau dihapus.
- Mencari dokumen berdasarkan kata kunci.
- Menyimpan hasil pencarian ke file teks.
- Membuka file yang dipilih langsung dari aplikasi.
- Melihat dan mengelola folder yang diindeks.

## Persyaratan

- Python 3.x
- CustomTkinter
- PyPDF2

## Instalasi

1. Clone repository atau unduh kode sumber.
2. Instal paket Python yang diperlukan:
    ```sh
    pip install customtkinter PyPDF2
    ```

## Penggunaan

1. Jalankan aplikasi:
    ```sh
    python InSearch.py
    ```

2. Jendela utama InSearch akan muncul dengan bagian-bagian berikut:
    - **Pengindeksan**: Memungkinkan Anda untuk memilih folder untuk diindeks dan melihat folder yang diindeks.
    - **Pencarian Kata Kunci**: Memungkinkan Anda untuk mencari dokumen berdasarkan kata kunci.

### Pengindeksan

1. Masukkan jalur folder yang ingin Anda indeks di bidang "Folder Path".
2. Klik tombol "Index Files" untuk memulai pengindeksan file di folder yang ditentukan.
3. Klik tombol "Show Indexed Folders" untuk melihat folder yang diindeks di sidebar.

### Pencarian Kata Kunci

1. Masukkan kata kunci yang ingin Anda cari di bidang "Search Keyword(s)".
2. Klik tombol "Search" untuk mencari dokumen yang mengandung kata kunci yang ditentukan.
3. Hasil pencarian akan ditampilkan di listbox di bawah.
4. Pilih hasil dan klik tombol "Open Selected File" untuk membuka file.
5. Klik tombol "Save Results" untuk menyimpan hasil pencarian ke file teks.

## Catatan

Aplikasi ini saat ini dalam versi demo dan mungkin belum mencakup semua fitur atau menangani semua kasus tepi. Pembaruan di masa mendatang akan meningkatkan fungsionalitas dan menambahkan lebih banyak fitur.

## Lisensi

Written by Hilmi Abdullah https://github.com/Hlmdul