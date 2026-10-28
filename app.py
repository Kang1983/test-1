from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime
import uuid
import base64

app = Flask(__name__, static_folder='.')
CORS(app)

DB_PATH = 'athletes.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS athletes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT,
            school TEXT,
            aau TEXT,
            usatf TEXT,
            gpa TEXT,
            photo TEXT,
            personal_bests TEXT,
            registered_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS medals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            athlete_id TEXT,
            event TEXT,
            date TEXT,
            performance TEXT,
            meet TEXT,
            FOREIGN KEY (athlete_id) REFERENCES athletes(id)
        )
    ''')
    conn.commit()
    conn.close()

def generate_id():
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(chars[ord(os.urandom(1)) % len(chars)] for _ in range(8))

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    athlete_id = generate_id()
    
    # Ensure unique
    conn = get_db()
    while conn.execute('SELECT 1 FROM athletes WHERE id = ?', (athlete_id,)).fetchone():
        athlete_id = generate_id()
    
    photo = data.get('photo')  # base64 string or null
    
    conn.execute('''
        INSERT INTO athletes (id, name, grade, school, aau, usatf, gpa, photo, personal_bests, registered_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        athlete_id,
        data.get('name'),
        data.get('grade'),
        data.get('school'),
        data.get('aau'),
        data.get('usatf'),
        data.get('gpa'),
        photo,
        json.dumps(data.get('personalBests', [])),
        datetime.utcnow().isoformat()
    ))
    
    # Add medal if provided
    medal = data.get('medal')
    if medal:
        conn.execute('''
            INSERT INTO medals (athlete_id, event, date, performance, meet)
            VALUES (?, ?, ?, ?, ?)
        ''', (athlete_id, medal.get('event'), medal.get('date'), medal.get('performance'), medal.get('meet')))
    
    conn.commit()
    conn.close()
    return jsonify({'id': athlete_id, 'success': True})

@app.route('/api/athlete/<athlete_id>', methods=['GET'])
def get_athlete(athlete_id):
    conn = get_db()
    athlete = conn.execute('SELECT * FROM athletes WHERE id = ?', (athlete_id.upper(),)).fetchone()
    if not athlete:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    
    medals = conn.execute('SELECT event, date, performance, meet FROM medals WHERE athlete_id = ?', (athlete_id.upper(),)).fetchall()
    conn.close()
    
    result = dict(athlete)
    result['personalBests'] = json.loads(result['personal_bests'] or '[]')
    result['medals'] = [dict(m) for m in medals]
    del result['personal_bests']
    return jsonify(result)

@app.route('/api/add-medal', methods=['POST'])
def add_medal():
    data = request.json
    athlete_id = data.get('athleteId', '').upper()
    medal = data.get('medal')
    
    conn = get_db()
    athlete = conn.execute('SELECT 1 FROM athletes WHERE id = ?', (athlete_id,)).fetchone()
    if not athlete:
        conn.close()
        return jsonify({'error': 'Athlete not found'}), 404
    
    conn.execute('''
        INSERT INTO medals (athlete_id, event, date, performance, meet)
        VALUES (?, ?, ?, ?, ?)
    ''', (athlete_id, medal.get('event'), medal.get('date'), medal.get('performance'), medal.get('meet')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/athletes', methods=['GET'])
def get_all_athletes():
    conn = get_db()
    athletes = conn.execute('SELECT * FROM athletes ORDER BY registered_at DESC').fetchall()
    result = []
    for a in athletes:
        athlete = dict(a)
        athlete['personalBests'] = json.loads(athlete['personal_bests'] or '[]')
        medals = conn.execute('SELECT event, date, performance, meet FROM medals WHERE athlete_id = ?', (a['id'],)).fetchall()
        athlete['medals'] = [dict(m) for m in medals]
        del athlete['personal_bests']
        result.append(athlete)
    conn.close()
    return jsonify(result)

@app.route('/api/coach-login', methods=['POST'])
def coach_login():
    data = request.json
    if data.get('username', '').lower() == 'coach' and data.get('password') == 'medal2026':
        return jsonify({'success': True})
    return jsonify({'success': False}), 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
