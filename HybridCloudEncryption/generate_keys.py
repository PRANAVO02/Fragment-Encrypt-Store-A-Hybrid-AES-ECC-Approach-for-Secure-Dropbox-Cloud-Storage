import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import secrets
from config import AES_KEY_FILE, ECC_PRIVATE_KEY_PATH, ECC_PUBLIC_KEY_PATH, AES_KEY_SIZE

os.makedirs("keys", exist_ok=True)

# --- Generate AES key ---
aes_key = secrets.token_bytes(AES_KEY_SIZE)
with open(AES_KEY_FILE, "wb") as f:
    f.write(aes_key)
print(f"✅ AES key generated at {AES_KEY_FILE}")

# --- Generate ECC key pair ---
private_key = ec.generate_private_key(ec.SECP384R1())
public_key = private_key.public_key()

# Save private key
with open(ECC_PRIVATE_KEY_PATH, "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save public key
with open(ECC_PUBLIC_KEY_PATH, "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print(f"✅ ECC key pair generated at {ECC_PRIVATE_KEY_PATH} and {ECC_PUBLIC_KEY_PATH}")
