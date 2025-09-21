from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Khởi tạo DB trong memory
def init_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.execute("INSERT INTO users (username, password) VALUES ('admin','admin123')")
    conn.commit()
    return conn

db = init_db()

@app.route("/")
def home():
    return "<h2>Welcome to DevSecOps Demo App 🚀</h2><p>Try /login?user=xxx&pass=xxx</p>"

# SQL Injection vulnerable endpoint
@app.route("/login")
def login():
    user = request.args.get("user", "")
    pwd = request.args.get("pass", "")
    query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"  # ❌ dễ bị SQLi
    cur = db.cursor()
    try:
        res = cur.execute(query).fetchone()
    except Exception as e:
        return f"SQL Error: {e}"
    if res:
        return f"<h3>✅ Login success! Hello {user}</h3>"
    else:
        return "❌ Login failed"

# XSS vulnerable endpoint
@app.route("/echo")
def echo():
    msg = request.args.get("msg", "Hello")
    return render_template_string(f"<h3>You said: {msg}</h3>")  # ❌ không sanitize → XSS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
