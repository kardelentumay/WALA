from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# --- DES Key Generation ---
def generate_des_key():
    return get_random_bytes(8)  # 8 byte = 64-bit

# --- Padding (ECB mode için gerekli) ---
def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    return text

# --- DES Encryption ---
def encrypt(message, key):
    des = DES.new(key, DES.MODE_ECB)
    padded_text = pad(message)
    encrypted = des.encrypt(padded_text.encode())
    return encrypted

# --- DES Decryption ---
def decrypt(ciphertext, key):
    des = DES.new(key, DES.MODE_ECB)
    decrypted = des.decrypt(ciphertext).decode().rstrip(' ')
    return decrypted

# --- RSA Encryption ---
def rsa_encrypt(message: bytes, public_key_path: str) -> bytes:
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message)

# --- RSA Decryption ---
def rsa_decrypt(ciphertext: bytes, private_key_path: str) -> bytes:
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)
