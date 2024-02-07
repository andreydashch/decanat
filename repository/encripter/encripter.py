from cryptography.fernet import Fernet

key = open("secret.key", "rb").read()
cipher_suite = Fernet(key)


def encrypt(text):
    text = text.encode("utf8")
    return cipher_suite.encrypt(text).decode()


def decrypt(text):
    text = text.encode("utf8")
    return cipher_suite.decrypt(text).decode()
