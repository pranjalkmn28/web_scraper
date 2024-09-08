from fastapi import Header, HTTPException
from config import settings

class Auth:
    @staticmethod
    def authenticate(authorization: str = Header(...)):
        if not authorization:
            raise HTTPException(status_code=403, detail="Authorization header missing")

        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Invalid token format. Should be 'Bearer <token>'")

        token = authorization.split(" ")[1]
        if token != settings.AUTH_TOKEN:
            raise HTTPException(status_code=403, detail="Invalid token")