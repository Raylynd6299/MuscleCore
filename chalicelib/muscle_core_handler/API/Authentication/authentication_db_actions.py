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
        print(first_name)
        print(last_name)
        print(email)
        print(password)
        print(salt_password)
        print(role_id)
        print(is_active)
        print(image_url)

        if not role_id:
            print("Role not provided")
            roles: List[Role] = Role.get(code="user")
            print ("Role: ", roles)
            
            if not roles:
                raise Exception({"error": "Roles not found."})
            
            role = roles[0]
            
            if not role or not isinstance(role, Role):
                raise Exception({"error": "Role not found."})
            
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
