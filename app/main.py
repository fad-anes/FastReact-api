from fastapi import FastAPI, HTTPException
from app.db.database import Base, engine
from app.users.routes import router as user_router
from app.products.routes import router as product_router
from app.AppFixtures import create_admin_user
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Initialisation de la base de données
Base.metadata.create_all(bind=engine)

# Chargement des variables d'environnement
load_dotenv()
app = FastAPI()

UPLOAD_DIR = "uploads"

# Vérification de la variable d'environnement CLIENT_URL
CLIENT_URL = os.getenv("CLIENT_URL")
if not CLIENT_URL:
    raise ValueError("Missing CLIENT_URL environment variable in .env file")

# CORS configuration
origins = [
    CLIENT_URL,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routeurs
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(product_router, prefix="/api", tags=["products"])

# Route pour servir les images
@app.get("/api/{image_name}")
async def get_image(image_name: str):
    file_path = os.path.join(UPLOAD_DIR, image_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

# Créer l'utilisateur administrateur au démarrage
create_admin_user()
