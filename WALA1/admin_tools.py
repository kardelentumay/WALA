from database import check_user, add_user
import sqlite3

def sysadmin_panel():
    print("🔐 SYSADMIN PANEL")

    username = input("Username: ")
    password = input("Password: ")

    if not check_user(username, password):
        print("❌ Unauthorized access!")
        return

    while True:
        print("\n📊 [1] List Users")
        print("➕ [2] Add new user")
        print("🗑️  [3] Delete User")
        print("📜 [4] Show Messages")
        print("🚪 [0] Exit")

        choice = input("Select: ")
        if choice == "1":
            show_users()
        elif choice == "2":
            new_user = input("New user's name: ")
            new_pass = input("password: ")
            add_user(new_user, new_pass)
        elif choice == "3":
            delete_user()
        elif choice == "4":
            show_messages()
        elif choice == "0":
            break
        else:
            print("Invalid selection.")

def show_users():
    conn = sqlite3.connect("wala.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users")
    users = c.fetchall()
    print("\n👥 Users:")
    for user in users:
        print("- " + user[0])
    conn.close()

def delete_user():
    uname = input("Name of the user to be deleted: ")
    conn = sqlite3.connect("wala.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (uname,))
    conn.commit()
    print(f"🗑️  User '{uname}' deleted.")
    conn.close()

def show_messages():
    conn = sqlite3.connect("wala.db")
    c = conn.cursor()
    c.execute("SELECT sender, receiver, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10")
    logs = c.fetchall()
    print("\n📝 Last 10 Mesagge:")
    for row in logs:
        print(f"[{row[3]}] {row[0]} → {row[1]}: {row[2]}")
    conn.close()
