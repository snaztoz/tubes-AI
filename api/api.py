from fastapi import FastAPI
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
