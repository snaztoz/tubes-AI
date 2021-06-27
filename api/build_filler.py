import os


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_FILLER_DIR = os.path.join(CURRENT_DIR, 'fill')

FILLER = {
    'jurusan': os.path.join(DATA_FILLER_DIR, 'jurusan.txt'),
    'jurusan_per_tahun': os.path.join(DATA_FILLER_DIR, 'jurusan_per_tahun.txt'),
    'pendaftaran': os.path.join(DATA_FILLER_DIR, 'pendaftaran.txt'),
}


# Untuk awalan, semua data disimpan dalam bentuk
# dictionary untuk memudahkan proses pencarian
# foreign key
unique_jurusan = {}
unique_jurusan_tahun = {}
pendaftaran = {}


with open(FILLER['jurusan']) as f:
    unique_lines = set()
    for line in f:
        unique_lines.add(line.strip())

    for i, pt_jurusan in enumerate(unique_lines):
        splitted = pt_jurusan.split('/')
        pt      = splitted[0]
        jurusan = splitted[1]

        unique_jurusan[f'{pt}_{jurusan}'] = (i + 1, pt, jurusan)


with open(FILLER['jurusan_per_tahun']) as f:
    unique_lines = set()
    for line in f:
        unique_lines.add(line.strip())

    for i, pt_jurusan_tahun in enumerate(unique_lines):
        splitted = pt_jurusan_tahun.split('/')
        pt_jurusan  = splitted[0]
        tahun       = int(splitted[1])
        keketatan   = float(splitted[2].replace(',', '.'))

        splitted_pt_jurusan = pt_jurusan.split('_')
        pt       = splitted_pt_jurusan[0]
        jurusan  = splitted_pt_jurusan[1]

        unique_jurusan_tahun[f'{tahun}_{pt}_{jurusan}'] = (
            i + 1,
            unique_jurusan[pt_jurusan][0],
            tahun,
            keketatan
        )


with open(FILLER['pendaftaran']) as f:
    # Semua data di sini sudah unik, tidak perlu dimasukkan
    # ke dalam set lagi.

    for line in f:
        stripped_line = line.strip().split('/')
        kode_pendaftar   = stripped_line[0]
        nilai            = float(stripped_line[1].replace(',', '.'))
        tahun_pt_jurusan = stripped_line[2]
        hasil            = stripped_line[3].upper()
        rank             = float(stripped_line[4])

        pendaftaran[kode_pendaftar] = (
            kode_pendaftar,
            nilai,
            rank,
            unique_jurusan_tahun[tahun_pt_jurusan][0],
            1 if hasil == 'DITERIMA' else 0
        )


def get_serialized_data():
    return {
        'Jurusan': [str(data) for data in unique_jurusan.values()],
        'JurusanPerTahun': [str(data) for data in unique_jurusan_tahun.values()],
        'Pendaftaran': [str(data) for data in pendaftaran.values()]
    }


def build_sql(data):
    sql = ''
    for table_name, rows in data.items():
        sql += f'INSERT INTO {table_name} VALUES '
        sql += ', '.join(rows)
        sql += ';\n'

    with open('filler.sql', 'w') as f:
        f.write(sql)


if __name__ == '__main__':
    serialized = get_serialized_data()
    build_sql(serialized)
