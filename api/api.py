from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3

import classifier


CURRENT_YEAR = 2021
CURRENT_YEAR_TOTAL_APPLICANTS = 303


conn = sqlite3.connect('data-snmptn.db')
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])


@app.get('/')
async def index():
    return {'message': 'It Works!'}


@app.get('/list-universitas')
async def get_universitas():
    cursor = conn.cursor()

    result = []
    cursor.execute('''
        SELECT DISTINCT
            pt
        FROM
            Jurusan
        JOIN
            JurusanPerTahun ON JurusanPerTahun.id_jurusan = Jurusan.id
        WHERE
            tahun = :year;
        ''',
        {'year': CURRENT_YEAR}
    )

    for row in cursor.fetchall():
        result.append(row[0])

    cursor.close()
    return {'list-universitas': result}


@app.get('/list-jurusan')
async def get_jurusan(universitas: Optional[str] = None):
    cursor = conn.cursor()

    query_result = []
    result = []

    if universitas:
        query_result = cursor.execute('''
            SELECT DISTINCT
                jurusan_fakultas
            FROM
                Jurusan
            JOIN
                JurusanPerTahun ON JurusanPerTahun.id_jurusan = Jurusan.id
            WHERE
                pt = :pt AND tahun = :year
            ''',
            {'pt': universitas, 'year': CURRENT_YEAR}
        )
    else:
        query_result = cursor.execute('SELECT DISTINCT jurusan_fakultas FROM Jurusan')

    for row in query_result:
        result.append(row[0])

    cursor.close()
    return {'list-jurusan': result}


@app.get('/predict')
async def predict(nilai: float, rank: int, universitas: str, jurusan: str):
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            keketatan
        FROM
            JurusanPerTahun
        JOIN
            Jurusan ON Jurusan.id = JurusanPerTahun.id_jurusan
        WHERE
            tahun = :year
            AND pt = :pt
            AND jurusan_fakultas = :jurusan; 
        ''',
        {'year': CURRENT_YEAR, 'pt': universitas, 'jurusan': jurusan}
    )

    (keketatan) = cursor.fetchone()[0]
    rank = (CURRENT_YEAR_TOTAL_APPLICANTS + 1 - rank) / CURRENT_YEAR_TOTAL_APPLICANTS

    # jalankan logika klasifikasi
    result = classifier.classify((keketatan, nilai, rank))

    cursor.close()
    return {'result': 'DITERIMA' if result == 1 else 'TIDAK DITERIMA'}
