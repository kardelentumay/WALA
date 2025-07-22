import socket
import threading
from crypto_utils import decrypt, encrypt, rsa_decrypt
from database import init_db, check_user, log_message
from rsa_auto_rotate import auto_generate_rsa_keys

auto_generate_rsa_keys()
init_db()

admin_mode = input("🔧 Log in as SysAdmin ? (y/n): ").lower()
if admin_mode == 'y':
    from admin_tools import sysadmin_panel
    sysadmin_panel()
    exit()

username = input("🔐 Server username: ")
password = input("🔐 Password: ")

if not check_user(username, password):
    print("❌ Invalid user info.")
    exit()
print("✅ Logged in.")

HOST = '0.0.0.0'
PORT = 12345

def receive_messages(conn, key):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            decrypted = decrypt(data, key)
            log_message(sender="client", receiver=username, message=decrypted)
            print(f"🟢 Client: {decrypted}")
        except Exception as e:
            print("❌ receive_messages error:", e)
            break

def send_messages(conn, key):
    while True:
        try:
            message = input("🔵 Server (message): ")
            if message == "":
                break
            encrypted = encrypt(message, key)
            conn.sendall(encrypted)
            log_message(sender=username, receiver="client", message=message)
        except Exception as e:
            print("❌ send_messages error:", e)
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("🟢 Server ready , waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print(f"🔗 Connected: {addr}")
        try:
            with open("rsa_keys/public_key.pem", "rb") as f:
                pub_key_data = f.read()
            print("📤 Public key file rewas read successfully . Size:", len(pub_key_data))
            conn.sendall(pub_key_data)
            print("📡 Public key sended to client.")

            encrypted_key = b''
            while len(encrypted_key) < 256:
                part = conn.recv(256 - len(encrypted_key))
                if not part:
                    raise ValueError("missing key retrieval")
                encrypted_key += part

            key = rsa_decrypt(encrypted_key, "rsa_keys/private_key.pem")
            print("✅ DES key solved.")
            print("🧪 Server DES Key:", key)

        except Exception as e:
            print("❌ key solving error:", e)
            conn.close()
            exit()

        threading.Thread(target=receive_messages, args=(conn, key), daemon=True).start()
        send_messages(conn, key)
