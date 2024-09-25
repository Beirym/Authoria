import os
import hashlib

def generateSalt() -> bytes:
    return os.urandom(16)

def hashPassword(password: str, salt: bytes = None) -> tuple[str, str]:
    if salt is None:
        salt = generateSalt()
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key.hex(), salt.hex()

def checkPassword(provided_password: str, stored_password: str, salt: str) -> bool:
    hashed_password = hashPassword(provided_password, bytes.fromhex(salt))[0]
    return stored_password == hashed_password