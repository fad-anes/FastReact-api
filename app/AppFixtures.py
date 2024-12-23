import os
from app.db.database import SessionLocal
from app.users.models import User
from app.utils import hash_password
from dotenv import load_dotenv


load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PWD = os.getenv("ADMIN_PWD")


if not ADMIN_USERNAME or not ADMIN_EMAIL or not ADMIN_PWD:
    raise ValueError("Admin credentials are missing in the environment variables")

def create_admin_user():
   
    db = SessionLocal()
    try:
      
        admin_user = db.query(User).filter(User.role == "admin").first()
        if not admin_user:
           
            new_admin = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PWD),
                role="admin",
                isactive=True,
            )
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            print(f"Admin user created: {new_admin.username}")
        else:
            print("Admin user already exists.")
    finally:
        db.close()
