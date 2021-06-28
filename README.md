# Project Tubes Artificial Intelligence
Project implementasi Artificial Intelligence untuk merekomendasikan persentase pilihan SNMPTN berdasarkan nilai rata-rata rapot.

## Requirements
1. Python 3
2. SQLite 3

## Step untuk menjalankan
1. Buka command line
2. Pindah ke directory api/
3. Jalankan perintah: `python -m venv venv`
4. Aktifkan virtual environment dengan menggunakan perintah: `venv\Scripts\Activate.bat`
5. Install requirements modul yang dibutuhkan program: `pip install -r requirements.txt`
6. Buat database baru dan beri nama 'data-snmptn.db': `sqlite3 data-snmptn.db`
7. Dari perintah sebelumnya, CLI akan masuk ke dalam program SQLite, kemudian selagi masih di dalam CLI SQLite, masukkan perintah berikut: `.read skema.sql`, kemudian jalankan: `.read filler.sql`
8. Keluar dari SQLite menggunakan perintah: `.quit`
9. Kemudian, jalankan perintah: `uvicorn api:app --reload`
10. Buka file HTML yang terletak di parent directory melalui browser (`../index.html`)