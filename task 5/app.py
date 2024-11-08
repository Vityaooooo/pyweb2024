from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

@app.route('/')
def hello():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO table_counter (datetime, client_info) VALUES (%s, %s) RETURNING id;",
            (datetime.now(), request.headers.get('User-Agent'))
        )
        count = cursor.fetchone()[0]
        conn.commit()
    conn.close()
    return f'Hello World! I have been seen {count} times.\n'

@app.route('/table_counter', methods=['GET'])
def get_table_counter():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, datetime, client_info FROM table_counter;")
        rows = cursor.fetchall()
    conn.close()

    table = []
    for row in rows:
        table.append({
            "id": row[0],
            "datetime": row[1].strftime('%Y-%m-%d %H:%M:%S'),  # Преобразуем дату в строку
            "client_info": row[2]
        })
    
    return jsonify(table)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
