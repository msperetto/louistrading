import base64
from getpass import getpass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from common.dao import database_operations as db

class Login():
    def __init__(self, exchange):
        self.exchange = exchange

    def create_cryptography_key(self):
        password_provided = getpass("Enter your cryptography password: ")
        password = password_provided.encode()
        salt = b'\xb5\x17H1\xbf\x9c\xe9\tp\xa8j_vcr='
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return Fernet(base64.urlsafe_b64encode(kdf.derive(password)))


    def save_sign_pair(self):
        f_key = self.create_cryptography_key()
        id = input(f"Enter {self.exchange} apikey id: ")
        sk = getpass(f"Enter {self.exchange} key: ").encode()
        encrypted = f_key.encrypt(sk).decode()
        db.insert_exchange_config(id, encrypted, self.exchange)
        return f_key


    def get_sign_pair(self, fernet_k):
        sign_pair = db.get_exchange_config(self.exchange)
        encrypted_sk = sign_pair["sk"].encode()
        decr_sk = fernet_k.decrypt(encrypted_sk)
        return sign_pair["id"], decr_sk


    def login_database(self):
        #Getting id and key from exchange
        if db.get_exchange_config(self.exchange):
            f_key = self.create_cryptography_key()
            self.e_id, self.e_sk = self.get_sign_pair(f_key)
        else:
            f_key = self.save_sign_pair()
            self.e_id, self.e_sk = self.get_sign_pair(f_key)
