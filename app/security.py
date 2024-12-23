from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from datetime import datetime
import os
from app.db.database import get_db
from app.users.models import User

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Schéma personnalisé pour accepter un Bearer token
http_bearer = HTTPBearer()

def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    token = authorization.credentials
    try:
        # Décodez le token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=403, detail="Token is invalid")

        # Récupérez l'utilisateur depuis la base de données
        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Vérifiez si le token est expiré
        if "exp" in payload and datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")

        return user
    except jwt.exceptions.PyJWTError:
        raise HTTPException(status_code=403, detail="Token is invalid")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":  
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user
