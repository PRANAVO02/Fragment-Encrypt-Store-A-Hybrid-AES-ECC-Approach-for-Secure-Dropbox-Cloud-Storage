import os, shutil, dropbox
from utils.crypto_aes import aes_decrypt
from utils.crypto_ecc import decrypt_aes_key
from utils.metadata import load_registry
from config import *

dbx = dropbox.Dropbox(ACCESS_TOKEN)

def decrypt_and_reconstruct(filename):
    """Download fragments from Dropbox and reconstruct original file"""
    registry = load_registry()
    if filename not in registry:
        raise Exception("File not found in registry")

    manifest = registry[filename]

    # Prepare download folder
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # Decrypt AES key
    enc_aes_key = bytes.fromhex(manifest["enc_aes_key"])
    ephemeral_pub = bytes.fromhex(manifest["ephemeral_pub"])
    with open(ECC_PRIVATE_KEY_PATH, "rb") as f:
        aes_key = decrypt_aes_key(enc_aes_key, ephemeral_pub, ECC_PRIVATE_KEY_PATH)

    # Download & decrypt fragments
    fragments = sorted(manifest["fragments"], key=lambda x: x["index"])
    reconstructed = b""

    for frag in fragments:
        frag_name = frag["name"]
        dropbox_path = f"{DROPBOX_FOLDER}/{frag_name}"

        metadata, res = dbx.files_download(dropbox_path)
        reconstructed += aes_decrypt(res.content, aes_key)

    # Save reconstructed file
    os.makedirs(RECONSTRUCTED_FOLDER, exist_ok=True)
    reconstructed_filename = f"reconstructed_{manifest['original_filename']}"
    reconstructed_path = os.path.join(RECONSTRUCTED_FOLDER, reconstructed_filename)
    with open(reconstructed_path, "wb") as f:
        f.write(reconstructed)

    return reconstructed_path
