import os
import jwt
import hashlib
from pony.orm import db_session
from chalice.app import Request
from typing import Dict, Optional
from chalicelib.db.entities import User
from .authentication_db_actions import MuscleCoreAPIAuthenticationDBActionsHandler


class MuscleCoreAPIAuthenticationHandler:
    def __init__(self, api_handler):
        self.api_handler = api_handler
        self.auth_bd_actions = MuscleCoreAPIAuthenticationDBActionsHandler()

        self.auth_secret_key = os.environ.get("AUTH_SECRET_KEY", "")

        self.iterations = 100000
        self.key_length = 64
        self.digest = "sha512"

    # Billing Information
    @db_session
    def user_handler(self, request: Optional[Request]) -> Optional[Dict]:
        if not request:
            raise Exception({"error": "No request provided"})

        try:
            if request.method == "POST":
                return self.post_user(request)
            else:
                raise Exception({"error": "Method not allowed"})
        except Exception as e:
            error_message = f"Error while processing muscle core info. Exception {e}"
            print(error_message)
            print(e)
            raise Exception({"error": error_message})

    @db_session
    def post_user(self, request):

        # get payload
        payload = self.post_user_validation(request)

        # get password to save
        password_hash, salt = self.get_password_to_save(payload.get("password", ""))

        # remove password from payload
        payload.pop("password")

        try:
            user = self.auth_bd_actions.create_user(
                **payload, password=password_hash, salt_password=salt
            )

            print("User created")
            print(user)

            if not user:
                raise Exception({"error": "Error while creating user."})
            if not isinstance(user, User):
                raise Exception({"error": "Error while creating user."})

            response = {
                "user": user.to_dict(),
                "token": self.encode_authentication_jwt(user.user_id),
            }

            print(response)

            return response
        except Exception as e:
            raise Exception({"error": f"Error while creating user. Exception: {e}"})

    def post_user_validation(self, request: Optional[Request]) -> Dict:
        if not request:
            raise Exception({"error": "No request provided."})

        payload = dict(request.json_body or {})

        new_payload = {}

        new_payload["email"] = payload.get("email", None)
        new_payload["first_name"] = payload.get("first_name", None)
        new_payload["last_name"] = payload.get("last_name", None)
        new_payload["image_url"] = payload.get("image_url", None)
        new_payload["password"] = payload.get("password", None)

        if not new_payload["email"]:
            raise Exception({"error": "Email is required."})

        if not new_payload["first_name"]:
            raise Exception({"error": "First name is required."})

        if not new_payload["last_name"]:
            raise Exception({"error": "Last name is required."})

        if not new_payload["password"]:
            raise Exception({"error": "Password is required to create a user."})

        # remove empty values
        return {k: v for k, v in new_payload.items() if v is not None}

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

    def get_password_to_save(self, password: str):
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
