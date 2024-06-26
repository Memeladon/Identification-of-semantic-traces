from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .database.config import PONY_ORM_CONFIG
from .database.register import register_pony_orm

from .routes.pages import pageRouter
from .settings import Settings
from .routes import chats, site_users



app = FastAPI(title=Settings.PROJECT_NAME, version=Settings.PROJECT_VERSION)

# ------------ Routing ------------ #
# app.mount("/staticfiles", StaticFiles(directory="./staticfiles"), name="staticfiles")
app.include_router(pageRouter)

# ---------- Middleware ---------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chats.router)
app.include_router(site_users.router)

# Регистрация Pony ORM
register_pony_orm(app, PONY_ORM_CONFIG, generate_schemas=True)

@app.get("/")
def home():
    return "Hello, World!"

