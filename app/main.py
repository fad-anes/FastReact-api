from fastapi import FastAPI
from app.db.database import Base, engine
from app.users.routes import router as user_router
from app.products.routes import router as product_router
from app.AppFixtures import create_admin_user 
from fastapi.responses import FileResponse
import os 


Base.metadata.create_all(bind=engine)

app = FastAPI()
UPLOAD_DIR = "uploads"

app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(product_router, prefix="/api", tags=["products"])
@app.get("/api/{image_name}")
async def get_image(image_name: str):
    file_path = os.path.join(UPLOAD_DIR, image_name)
    if not os.path.exists(file_path):
        return {"error": "Image not found"}
    return FileResponse(file_path)

create_admin_user()
