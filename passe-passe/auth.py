import os
import sys
import subprocess
import json
from Crypto.Cipher import AES
import scrypt


def _getpass(prompt="Enter value: \n"):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    subprocess.check_call(["stty","-echo"])
    byte_input = input().encode()
    subprocess.check_call(["stty","echo"])
    return byte_input

def encrypt_AES(pw, credentials):
    json_bytes = json.dumps(credentials, indent=2).encode()
    kdfsalt = os.urandom(16)
    secret_key = scrypt.hash(pw, salt=kdfsalt, N=131072, r=8, p=1, buflen=32)
    aes_cipher = AES.new(secret_key, AES.MODE_GCM)
    ciphertext, mac = aes_cipher.encrypt_and_digest(json_bytes)
    return {"cipher": "AES.MODE_GCM", "kdfsalt": kdfsalt, "ciphertext": ciphertext, "nonce": aes_cipher.nonce, "mac" : mac}

def decrypt_AES(pw, kdfsalt, ciphertext, nonce, mac):
    secret_key = scrypt.hash(pw, salt=kdfsalt, N=131072, r=8, p=1, buflen=32)
    aes_cipher = AES.new(secret_key, AES.MODE_GCM, nonce)
    json_bytes = aes_cipher.decrypt_and_verify(ciphertext, mac)
    return json_bytes.decode()
