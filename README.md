# Fragment-Encrypt-Store: A Hybrid AES–ECC Approach for Secure Dropbox Cloud Storage  

## 📌 Overview  
This project implements a **secure cloud storage system** using a **hybrid AES–ECC encryption model**.  
- Files are **split into fragments**,  
- Each fragment is **encrypted using AES (symmetric encryption)**,  
- The AES key is further **encrypted with ECC (asymmetric encryption)**,  
- All encrypted fragments and metadata are stored securely in **Dropbox Cloud**.  

A **Flask-based web UI** allows users to upload, download, and reconstruct files seamlessly.  

---

## 🚀 Features  
✅ **Hybrid Encryption** → Combines AES (fast) with ECC (secure key exchange).  
✅ **File Fragmentation** → Breaks files into multiple encrypted parts for added security.  
✅ **Dropbox Cloud Integration** → Stores and retrieves encrypted fragments from Dropbox.  
✅ **Flask Web Interface** → Easy-to-use dashboard for upload & download.  
✅ **Secure Reconstruction** → Ensures files can only be decrypted with the correct ECC key.  

---

## 🏗️ System Architecture  

```plaintext
User File → Split into Fragments → AES Encryption → AES Key Encrypted with ECC → Upload to Dropbox  
                                                                                  ↓  
                                      Download from Dropbox ← AES Key Decrypted with ECC ← Reconstruct File
