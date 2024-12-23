from fastapi import FastAPI
from app.db.database import Base, engine
from app.users.routes import router as user_router
from app.AppFixtures import create_admin_user  


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(user_router, prefix="/api", tags=["users"])


create_admin_user()
