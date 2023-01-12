from jwt import encode
from dotenv import load_dotenv
import os

load_dotenv()


def create_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token
