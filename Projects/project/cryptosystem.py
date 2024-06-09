from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
# Tạo cặp khóa ECC
def generate_ecc_key_pair():
    private_key = ec.generate_private_key(
        ec.SECP256R1(), default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Tạo khóa chia sẻ từ khóa công khai của người nhận và khóa bí mật của người gửi
def derive_shared_key(private_key_sender, public_key_recipient):
    shared_key = private_key_sender.exchange(ec.ECDH(), public_key_recipient)
    return shared_key

# Mã hóa dữ liệu sử dụng khóa chia sẻ
def encrypt_data(data, shared_key):
    # Tạo một salt ngẫu nhiên
    salt = b"some_random_salt"
    # Sử dụng HKDF để tạo khóa dùng cho AES-GCM
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"encryption key",
        backend=default_backend()
    ).derive(shared_key)

    # Mã hóa dữ liệu sử dụng AES-GCM
    cipher = AESGCM(derived_key)
    nonce = os.urandom(12)
    ciphertext = cipher.encrypt(nonce, data, None)
    return ciphertext, nonce

# Giải mã dữ liệu sử dụng khóa chia sẻ
def decrypt_data(ciphertext, shared_key, nonce):
    # Tạo một salt ngẫu nhiên
    salt = b"some_random_salt"
    # Sử dụng HKDF để tạo khóa dùng cho AES-GCM
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"encryption key",
        backend=default_backend()
    ).derive(shared_key)

    # Giải mã dữ liệu sử dụng AES-GCM
    cipher = AESGCM(derived_key)
    plaintext = cipher.decrypt(nonce, ciphertext, None)
    return plaintext

# Sử dụng
private_key_sender, public_key_sender = generate_ecc_key_pair()
private_key_recipient, public_key_recipient = generate_ecc_key_pair()

# Tạo khóa chia sẻ từ khóa công khai của người nhận và khóa bí mật của người gửi
shared_key = derive_shared_key(private_key_sender, public_key_recipient)

# Dữ liệu cần mã hóa
data = b"Hello, world!"

# Mã hóa dữ liệu
ciphertext, nonce = encrypt_data(data, shared_key)

# Giải mã dữ liệu
plaintext = decrypt_data(ciphertext, shared_key, nonce)


print("Original data:", data)
print("Encrypted data",ciphertext.hex())
print("Decrypted data:", plaintext)
print("Nonce",nonce.hex())
