import socket
import threading
from crypto_utils import encrypt, decrypt, rsa_encrypt, generate_des_key
from database import init_db, log_message

init_db()

HOST = '192.168.0.111'
PORT = 12345
username = input("🔐 Username: ")

def receive_messages(sock, key):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            decrypted = decrypt(data, key)
            log_message(sender="server", receiver=username, message=decrypted)
            print(f"🟢 Server: {decrypted}")
        except Exception as e:
            print("❌ receive_messages error:", e)
            break

def send_messages(sock, key):
    while True:
        try:
            message = input("🔵 Client (message): ")
            if message == "":
                break
            encrypted = encrypt(message, key)
            sock.sendall(encrypted)
            log_message(sender=username, receiver="server", message=message)
        except Exception as e:
            print("❌ send_messages error:", e)
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("📡 Waiting public key from Server...")

    pub_key = s.recv(1024)
    print("✅ Public key received. Size:", len(pub_key))

    with open("temp_public_key.pem", "wb") as f:
        f.write(pub_key)

    des_key = generate_des_key()
    print("🧪 Client DES Key:", des_key)
    encrypted_key = rsa_encrypt(des_key, "temp_public_key.pem")
    s.sendall(encrypted_key)
    print("🔐 DES key send encrypted.")

    threading.Thread(target=receive_messages, args=(s, des_key), daemon=True).start()
    send_messages(s, des_key)