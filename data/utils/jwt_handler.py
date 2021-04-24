from datetime import datetime, timedelta
from typing import Dict
import jwt
import time

ALGORITHM = "HS256"
SECRET_KEY = "MYCOMPANY_secret"


def sign_jwt(user_id: str) -> Dict[str, str]:
    ACCESS_TOKEN_EXPIRE_DAYS = datetime.now() + timedelta(days=1)
    payload = {
        "user_id": user_id,
        "exp": ACCESS_TOKEN_EXPIRE_DAYS,
        "iat": datetime.now(),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception:
        return {}
