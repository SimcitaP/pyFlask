import csv
from werkzeug.security import generate_password_hash

from config import USER_FILE


def init_user_file():
    """Ensure the users.csv file exists with the correct headers."""
    try:
        with open(USER_FILE, "x", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["UserID", "Username", "PasswordHash", "RoleID", "Email"])
    except FileExistsError:
        pass


def find_user(username):
    """Find a user by username."""
    with open(USER_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Username"] == username:
                return row
    return None


def add_user(username, password, role="2", email="user@example.com"):
    """Add a new user with hashed password."""
    hashed = generate_password_hash(password)

    # Count existing users for UserID
    with open(USER_FILE, newline="") as f:
        user_count = sum(1 for _ in f)

    with open(USER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user_count, username, hashed, role, email])
