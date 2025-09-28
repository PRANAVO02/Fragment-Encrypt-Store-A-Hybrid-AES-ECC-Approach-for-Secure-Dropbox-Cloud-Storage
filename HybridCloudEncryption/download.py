import os, json, shutil
import dropbox
from utils.crypto_aes import aes_decrypt
from utils.crypto_ecc import decrypt_aes_key
from utils.metadata import load_registry
from config import *

dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Load registry
registry = load_registry()
if not registry:
    print("📂 No files available for download.")
    exit()

# List files
print("\n📂 Available files:")
for i, fname in enumerate(registry.keys(), start=1):
    print(f"{i}. {fname}")

choice = input("\nEnter filename to download: ").strip()
if choice not in registry:
    print(f"❌ File '{choice}' not found.")
    exit()

manifest = registry[choice]

# Prepare download folder
if os.path.exists(DOWNLOAD_FOLDER):
    shutil.rmtree(DOWNLOAD_FOLDER)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Decrypt AES key using ECC
enc_aes_key = bytes.fromhex(manifest["enc_aes_key"])
ephemeral_pub = bytes.fromhex(manifest["ephemeral_pub"])
with open(ECC_PRIVATE_KEY_PATH, "rb") as f:
    private_key_path = ECC_PRIVATE_KEY_PATH

from utils.crypto_ecc import decrypt_aes_key
with open(ECC_PRIVATE_KEY_PATH, "rb") as f:
    aes_key = decrypt_aes_key(enc_aes_key, ephemeral_pub, ECC_PRIVATE_KEY_PATH)

# Download & decrypt fragments
fragments = sorted(manifest["fragments"], key=lambda x: x["index"])
reconstructed = b""

print("\n⬇️ Downloading and decrypting fragments...")
for frag in fragments:
    frag_name = frag["name"]
    dropbox_path = f"{DROPBOX_FOLDER}/{frag_name}"
    local_path = os.path.join(DOWNLOAD_FOLDER, frag_name)

    metadata, res = dbx.files_download(dropbox_path)
    with open(local_path, "wb") as f:
        f.write(res.content)

    reconstructed += aes_decrypt(res.content, aes_key)
    print(f"   ✅ Fragment {frag_name} done")

# Save reconstructed file
os.makedirs(RECONSTRUCTED_FOLDER, exist_ok=True)
reconstructed_filename = f"reconstructed_{manifest['original_filename']}"
reconstructed_path = os.path.join(RECONSTRUCTED_FOLDER, reconstructed_filename)
with open(reconstructed_path, "wb") as f:
    f.write(reconstructed)

print(f"\n🎉 File reconstructed successfully: '{reconstructed_path}'")
