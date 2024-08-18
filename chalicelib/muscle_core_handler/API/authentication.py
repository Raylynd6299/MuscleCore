import os
import jwt
import hashlib


class MuscleCoreAPIAuthentication:
    def __init__(self, api_handler):
        self.api_handler = api_handler
        self.auth_secret_key = os.environ.get("AUTH_SECRET_KEY", "")

        self.iterations = 100000
        self.key_length = 64
        self.digest = "sha512"

    def decode_authentication_jwt(self, token):
        try:
            token_decoded = jwt.decode(
                token, self.auth_secret_key, algorithms=["HS256"]
            )
        except Exception:
            msg = {"error": "Token is invalid or expired."}
            raise Exception(msg)

        return token_decoded

    def encode_authentication_jwt(self, user_id):
        token = jwt.encode(
            {"user_id": user_id}, self.auth_secret_key, algorithm="HS256"
        )

        return token

    def get_password_to_save(self, password):
        salt = self.generate_salt()
        password_hash = self.hash_password(password, salt)

        return password_hash.hex(), salt.hex()
    
    def check_password(self, password, salt, password_hash):
        has_to_verify = self.hash_password(password, bytes.fromhex(salt))

        return has_to_verify == bytes.fromhex(password_hash)

    def hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac(
            self.digest, password.encode(), salt, self.iterations, dklen=self.key_length
        )
    
    def generate_salt(self):
        return os.urandom(self.key_length)
