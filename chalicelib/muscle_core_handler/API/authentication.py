import os
import jwt

class MuscleCoreAPIAuthentication:
    def __init__(self, api_handler):
        self.api_handler = api_handler
        self.auth_secret_key = os.environ.get("AUTH_SECRET_KEY", "")

    def decode_authentication_jwt(self, token):
        try:
            token_decoded = jwt.decode(token, self.auth_secret_key , algorithms=["HS256"])
        except Exception:
            msg = {"error": "Token is invalid or expired."}
            raise Exception(msg)

        return token_decoded
    