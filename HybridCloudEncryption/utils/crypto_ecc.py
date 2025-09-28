from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os


# Encrypt AES key using ECC public key
def encrypt_aes_key(aes_key: bytes, public_key_path: str) -> bytes:
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # ECDH key exchange
    ephemeral_key = ec.generate_private_key(ec.SECP384R1())
    shared_key = ephemeral_key.exchange(ec.ECDH(), public_key)

    # Derive symmetric key
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=len(aes_key),
        salt=None,
        info=b"encrypt-aes-key"
    ).derive(shared_key)

    # AES encrypt AES key
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(aes_key) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return iv + ciphertext, ephemeral_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


# Decrypt AES key using ECC private key
def decrypt_aes_key(enc_aes_key: bytes, ephemeral_pub_bytes: bytes, private_key_path: str) -> bytes:
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from cryptography.hazmat.primitives.asymmetric import ec

    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    ephemeral_pub = load_pem_public_key(ephemeral_pub_bytes)
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_pub)

    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"encrypt-aes-key"
    ).derive(shared_key)

    iv = enc_aes_key[:16]
    ct = enc_aes_key[16:]
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ct) + decryptor.finalize()
    from cryptography.hazmat.primitives import padding
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded) + unpadder.finalize()
