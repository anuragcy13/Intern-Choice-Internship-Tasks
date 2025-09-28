# app.py
import re, sqlite3, os
from flask import Flask, request, jsonify
from bcrypt import gensalt, hashpw, checkpw

DB = 'users.db'
COMMON = {"123456","password","123456789","12345678","qwerty","abc123","111111","123123"}

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    phone TEXT
                )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS pw_hist (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    pw_hash BLOB,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    con.commit(); con.close()

def validate_password(pw, username=None, phone=None):
    if len(pw) < 12:
        return False, "Password must be at least 12 characters."
    if not re.search(r'[A-Z]', pw):
        return False, "Must include an uppercase letter."
    if not re.search(r'[a-z]', pw):
        return False, "Must include a lowercase letter."
    if not re.search(r'[0-9]', pw):
        return False, "Must include a number."
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>\\[\\]\\/\'`~\\-+=;:_]', pw):
        return False, "Must include a special character."
    if pw.lower() in COMMON:
        return False, "Password is too common."
    low = pw.lower()
    if username and username.lower() in low:
        return False, "Must not contain username."
    if phone:
        digits = re.sub(r'\D','', phone)
        if digits and digits in low:
            return False, "Must not contain phone number."
    return True, "OK"

def hash_password(pw: str) -> bytes:
    salt = gensalt()  # bcrypt salt
    return hashpw(pw.encode('utf-8'), salt)

def check_reuse(user_id, pw_plain) -> bool:
    # return True if pw_plain matches any of last 5 hashes
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT pw_hash FROM pw_hist WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (user_id,))
    rows = cur.fetchall()
    con.close()
    for (h,) in rows:
        if checkpw(pw_plain.encode('utf-8'), h):
            return True
    return False

def store_password(user_id, pw_hash):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO pw_hist (user_id, pw_hash) VALUES (?, ?)", (user_id, pw_hash))
    # keep only last 10 rows per user (cleanup)
    cur.execute("""
      DELETE FROM pw_hist
      WHERE id IN (
        SELECT id FROM pw_hist WHERE user_id = ? ORDER BY created_at DESC LIMIT -1 OFFSET 10
      )
    """, (user_id,))
    con.commit(); con.close()

app = Flask(__name__)
init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    username = data.get('username')
    phone = data.get('phone')
    password = data.get('password')
    if not username or not password:
        return jsonify({"ok":False, "error":"username and password required"}), 400

    ok, msg = validate_password(password, username=username, phone=phone)
    if not ok:
        return jsonify({"ok":False, "error": msg}), 400

    con = sqlite3.connect(DB)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO users (username, phone) VALUES (?, ?)", (username, phone))
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # user exists — get user_id
        cur.execute("SELECT id FROM users WHERE username=?", (username,))
        r = cur.fetchone()
        user_id = r[0]
    con.commit(); con.close()

    # reuse check
    if check_reuse(user_id, password):
        return jsonify({"ok":False, "error":"Password was used recently. Choose a different one."}), 400

    # hash and store
    pw_hash = hash_password(password)
    store_password(user_id, pw_hash)

    return jsonify({"ok":True, "msg":"Registered / password updated successfully."})

if __name__ == "__main__":
    app.run(debug=True)
