from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sqlite3

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
    for row in cursor.execute('SELECT DISTINCT pt FROM Jurusan'):
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
            SELECT DISTINCT jurusan_fakultas FROM Jurusan WHERE pt=:pt
            ''',
            {'pt': universitas}
        )
    else:
        query_result = cursor.execute('SELECT DISTINCT jurusan_fakultas FROM Jurusan')

    for row in query_result:
        result.append(row[0])

    cursor.close()
    return {'list-jurusan': result}
