import re
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List  
from app.users.models import User
from app.users.schemas import UserCreate, UserResponse
from app.db.database import get_db
from app.utils import hash_password, verify_password, create_access_token
from app.users.schemas import Role  
from app.security import get_admin_user

router = APIRouter()

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérification du format de l'email
    if not re.match(EMAIL_REGEX, user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    # Création du nouvel utilisateur
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=Role.user,  # Par défaut rôle "user"
        isactive=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Renvoi de la réponse selon le schéma UserResponse
    return new_user

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Vérification du mot de passe
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Vérification si l'utilisateur est actif
    if not user.isactive:
        raise HTTPException(status_code=401, detail="Your account is not active")
    
    # Préparation des données de l'utilisateur pour le token
    user_data = {
        "id": user.id,
        "email": user.email,
        "username": user.username,  
        "role": user.role.value  
    }
    
    # Création du token d'accès
    access_token = create_access_token(data={"sub": user.email, **user_data})
    
    return {"access_token": access_token, "user": user_data}

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    # Récupérer tous les utilisateurs
    users = db.query(User).all()
    return users

@router.put("/users/toggle_status/{user_id}", response_model=UserResponse)
def toggle_user_status(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    # Récupérer l'utilisateur par ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Inverser le statut actif
    user.isactive = not user.isactive
    db.commit()
    db.refresh(user)
    
    return user
