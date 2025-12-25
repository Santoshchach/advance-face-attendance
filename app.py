import os
import sqlite3
import json
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
DB_PATH = os.path.join("database", "attendance.db")

def init_db():
    """Initialize the SQLite database with users and attendance tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    face_descriptor TEXT NOT NULL
                )''')
    
    # Attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    UNIQUE(user_id, date)
                )''')
    
    conn.commit()
    conn.close()

# Initialize Database on startup
if not os.path.exists("database"):
    os.makedirs("database")
init_db()

@app.route('/')
def index():
    """Module 1: Camera Access & Home Page"""
    return render_template('camera.html')

@app.route('/register')
def register_page():
    """Module 2: User Registration Page"""
    return render_template('register.html')

@app.route('/recognition')
def recognition_page():
    """Module 3: Live Face Recognition Page"""
    return render_template('recognition.html')

@app.route('/attendance/success')
def attendance_success():
    """Module 4: Attendance Success Page"""
    return render_template('attendance_success.html')

@app.route('/attendance/exists')
def attendance_exists():
    """Module 5: Attendance Exists Page"""
    return render_template('attendance_exists.html')

@app.route('/reports')
def reports_page():
    """Module 6: Reports Page"""
    return render_template('reports.html')

@app.route('/admin')
def admin_page():
    """Module 7: Admin Dashboard"""
    return render_template('admin.html')

# API Endpoints
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name')
    user_id = data.get('user_id')
    descriptor = data.get('descriptor') # List of floats
    
    if not name or not user_id or not descriptor:
        return jsonify({"success": False, "message": "Missing data"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (user_id, name, face_descriptor) VALUES (?, ?, ?)",
                  (user_id, name, json.dumps(descriptor)))
        conn.commit()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "User ID already exists"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "message": "Missing User ID"}), 400
    
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if user exists
    c.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({"success": False, "message": "User not found"}), 404
    
    user_name = user[0]
    
    try:
        c.execute("INSERT INTO attendance (user_id, date, time) VALUES (?, ?, ?)",
                  (user_id, date_str, time_str))
        conn.commit()
        return jsonify({"success": True, "name": user_name, "date": date_str, "time": time_str, "status": "marked"})
    except sqlite3.IntegrityError:
        return jsonify({"success": True, "name": user_name, "status": "exists"}), 200
    finally:
        conn.close()

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all registered users and their descriptors for frontend matching."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, name, face_descriptor FROM users")
    rows = c.fetchall()
    conn.close()
    
    users = []
    for r in rows:
        users.append({
            "user_id": r[0],
            "name": r[1],
            "descriptor": json.loads(r[2])
        })
    return jsonify(users)

@app.route('/api/records', methods=['GET'])
def get_records():
    """Get all attendance records joined with user names."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT u.name, u.user_id, a.date, a.time 
        FROM attendance a
        JOIN users u ON a.user_id = u.user_id
        ORDER BY a.date DESC, a.time DESC
    """)
    rows = c.fetchall()
    conn.close()
    
    records = []
    for r in rows:
        records.append({
            "name": r[0],
            "user_id": r[1],
            "date": r[2],
            "time": r[3]
        })
    return jsonify(records)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get admin stats."""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM attendance WHERE date = ?", (date_str,))
    present_today = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "total_users": total_users,
        "present_today": present_today
    })

@app.route('/api/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user and their face data from the system."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        if c.rowcount == 0:
            return jsonify({"success": False, "message": "User not found"}), 404
        conn.commit()
        return jsonify({"success": True, "message": f"User {user_id} deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
