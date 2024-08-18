from typing import List, Optional
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
        print("Creating user")

        if not role_id:
            role: Optional[Role] = Role.get(code="user")
            
            if not role:
                raise Exception({"error": "Roles not found."})
            
            role_id = str(role.role_id or "")	

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

    @db_session
    def get_user_by_email(self, email: str) -> Optional[User]:
        return User.get(email=email)