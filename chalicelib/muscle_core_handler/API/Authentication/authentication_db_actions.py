from typing import Optional
from pony.orm import db_session
from chalicelib.db.entities import User, Role


class MuscleCoreAPIAuthenticationDBActionsHandler:

    def __init__(self):
        pass

    @db_session
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        salt_password: str,
        role_id: Optional[str] = None,
        is_active: bool = True,
        image_url: Optional[str] = None,
    ) -> User:

        if not role_id:
            role_id = Role.get(code="user").role_id

        return User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            salt_password=salt_password,
            role=role_id,
            is_active=is_active,
            image_url=image_url,
        )
