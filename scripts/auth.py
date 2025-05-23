# scripts/auth.py
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 email TEXT PRIMARY KEY,
                 password TEXT,
                 created_at TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_logs (
                 email TEXT,
                 timestamp TEXT,
                 action TEXT,
                 query TEXT)''')
    conn.commit()
    conn.close()

# --- Helpers ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

def register_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)",
              (email, hash_password(password), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def log_user_action(email, action, query=None):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO user_logs (email, timestamp, action, query) VALUES (?, ?, ?, ?)",
              (email, datetime.utcnow().isoformat(), action, query))
    conn.commit()
    conn.close()

# --- UI Authentication ---
def login_ui():
    st.sidebar.title("🔐 Login or Register")
    auth_choice = st.sidebar.radio("Choose an option:", ["Login", "Register"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if auth_choice == "Register":
        if st.sidebar.button("Register"):
            register_user(email, password)
            st.sidebar.success("Account created. Please login.")

    elif auth_choice == "Login":
        if st.sidebar.button("Login"):
            if verify_user(email, password):
                st.session_state["authenticated"] = True
                st.session_state["user"] = email
                st.sidebar.success(f"Logged in as {email}")
                log_user_action(email, "login")
            else:
                st.sidebar.error("Invalid credentials.")

    return st.session_state.get("authenticated", False), st.session_state.get("user", None)

# Run once on startup
init_db()
