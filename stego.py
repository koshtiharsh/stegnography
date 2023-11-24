import cv2
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


def encrypt(message, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message) + padder.finalize()

    return encryptor.update(padded_message) + encryptor.finalize()


def decrypt(ciphertext, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    return unpadder.update(decrypted_message) + unpadder.finalize()


img = cv2.imread("mypic.jpg")

msg = input("Enter secret message: ")
password = input("Enter password: ")


key = os.urandom(32)  
encrypted_msg = encrypt(msg.encode(), key)

m = 0
n = 0
z = 0

for i in range(len(encrypted_msg)):
    img[n, m, z] = encrypted_msg[i]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3

cv2.imwrite("encrypted.jpg", img)
os.system("start encrypted.jpg")


message = b""
n = 0
m = 0
z = 0

pas = input("Enter passcode for Decryption: ")

if password == pas:
    for i in range(len(encrypted_msg)):
        message += bytes([img[n, m, z]])
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    decrypted_msg = decrypt(message, key)
    print("Decrypted message:", decrypted_msg.decode())
else:
    print("Not a valid key")
