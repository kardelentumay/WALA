from Crypto.PublicKey import RSA
import os

def auto_generate_rsa_keys(directory="rsa_keys"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    private_path = os.path.join(directory, "private_key.pem")
    public_path = os.path.join(directory, "public_key.pem")

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_path, "wb") as priv_file:
        priv_file.write(private_key)

    with open(public_path, "wb") as pub_file:
        pub_file.write(public_key)

    print("🔁 RSA keys renewed.")

if __name__ == "__main__":
    auto_generate_rsa_keys()
