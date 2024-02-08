from cryptography.fernet import Fernet

key = open("repository/encripter/secret.key", "rb").read()
cipher_suite = Fernet(key)


def encrypt(text):
    text = str(text).encode("utf8")
    return cipher_suite.encrypt(text).decode()


def decrypt(text):
    text = str(text).encode("utf8")
    return cipher_suite.decrypt(text).decode()
