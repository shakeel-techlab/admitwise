
import hashlib
import json
import os
import re

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")


def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(email, password, name, city=""):
    if not email or not password or not name:
        return False, "All fields are required."

    email = email.strip().lower()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email address."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = _load_users()
    if email in users:
        return False, "An account with this email already exists."

    users[email] = {
        "name": name.strip(),
        "email": email,
        "city": city.strip(),
        "password": _hash_password(password),
        "saved_universities": [],
        "profile": {},
    }
    _save_users(users)
    return True, "Account created successfully!"


def login_user(email, password):
    if not email or not password:
        return False, None, "Email and password are required."

    email = email.strip().lower()
    users = _load_users()

    if email not in users:
        return False, None, "No account found with this email."

    if users[email]["password"] != _hash_password(password):
        return False, None, "Incorrect password."

    return True, users[email], "Login successful!"


def update_user_profile(email, profile_data):
    users = _load_users()
    if email in users:
        users[email]["profile"] = profile_data
        _save_users(users)
        return True
    return False


def save_university(email, uni_id):
    users = _load_users()
    if email in users:
        saved = users[email].get("saved_universities", [])
        if uni_id not in saved:
            saved.append(uni_id)
            users[email]["saved_universities"] = saved
            _save_users(users)
        return True
    return False


def unsave_university(email, uni_id):
    users = _load_users()
    if email in users:
        saved = users[email].get("saved_universities", [])
        if uni_id in saved:
            saved.remove(uni_id)
            users[email]["saved_universities"] = saved
            _save_users(users)
        return True
    return False


def get_saved_universities(email):
    users = _load_users()
    if email in users:
        return users[email].get("saved_universities", [])
    return []
