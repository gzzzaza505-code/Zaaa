from flask import Flask, request, render_template, jsonify
import sqlite3
import datetime
import os

app = Flask(__name__)

DB_FILE = "bot_data.db"

def log_to_db(user_id, username, ip, user_agent, hardware):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO drac_logs (timestamp, user_id, username, ip, user_agent, hardware) VALUES (?, ?, ?, ?, ?, ?)",
              (datetime.datetime.now().isoformat(), user_id, username, ip, user_agent, hardware))
    conn.commit()
    conn.close()

@app.route('/verify/<int:user_id>/<username>')
def verify_page(user_id, username):
    return render_template('verify.html', user_id=user_id, username=username)

@app.route('/api/verify', methods=['POST'])
def api_verify():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    hardware = data.get('hardware', 'Unknown')
    
    log_to_db(user_id, username, ip, user_agent, hardware)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Initialize log table if not exists
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS drac_logs 
                    (timestamp TEXT, user_id INTEGER, username TEXT, ip TEXT, user_agent TEXT, hardware TEXT)''')
    conn.close()
    app.run(host='0.0.0.0', port=5000)
