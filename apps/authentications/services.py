from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from typing import Optional, Tuple
from config.settings.base import SIMPLE_JWT
from apps.member_management.models import Member
import bcrypt
import jwt
from datetime import datetime, timedelta


class LoginService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        user = authenticate(username=username, password=password)
        return user

    @staticmethod
    def generate_access_token(member:Member) -> str:
        payload = {
            'user_id': member.member_id,
            'username': member.username,
            'email': member.email,
            'exp': datetime.utcnow() + timedelta(minutes=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']),  # Use timedelta for expiration
            'iat': datetime.utcnow(),
        }
        encoded_jwt = jwt.encode(payload, SIMPLE_JWT['SECRETE_KEY'], algorithm=SIMPLE_JWT['JWT_ALGORITHM'])
        return encoded_jwt
    
    @staticmethod
    def check_password(provided_password:str, stored_hashed_password:str) -> bool:
        """
        Checks if the provided password matches the stored hashed password.
        """
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))