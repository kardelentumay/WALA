from database import add_user, init_db

init_db()  # <-- Eksik olan satır

print("👤 Create new user")
username = input("Username: ")
password = input("Password: ")

add_user(username, password)
print(f"✅ User '{username}' added successfully.")
