from Crypto.Cipher import AES
import base64


def encrypt(msg, secret_key):
    msg = str.encode(msg)
    msg_text = msg.rjust(next16mult(len(msg)))
    secret_key = str.encode(secret_key.rjust(16))

    cipher = AES.new(secret_key, AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded.decode("utf-8")


def next16mult(length):
    mult = 0
    while True:
        mult += 16
        if mult >= length:
            return mult


def decrypt(encoded, secret_key):
    cipher = AES.new(str.encode(secret_key.rjust(16)), AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(encoded))
    return decoded.strip().decode("utf-8")
