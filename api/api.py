from fastapi import FastAPI
from typing import Optional
import sqlite3

conn = sqlite3.connect('data-snmptn.db')
app = FastAPI()


@app.get('/')
async def index():
    return {'message': 'It Works!'}


@app.get('/list-universitas')
async def get_universitas():
    cursor = conn.cursor()

    result = []
    for row in cursor.execute('SELECT DISTINCT universitas FROM Jurusan'):
        result.append(row[0])

    cursor.close()
    return {'list-universitas': result}


@app.get('/list-jurusan')
async def get_jurusan(universitas: Optional[str] = None):
    cursor = conn.cursor()

    query_result = []
    result = []

    if universitas:
        query_result = cursor.execute(
            'SELECT DISTINCT nama FROM Jurusan WHERE universitas=?',
            universitas
        )
    else:
        query_result = cursor.execute('SELECT nama FROM Jurusan')

    for row in query_result:
        result.append(row[0])

    return {'list-jurusan': result}
