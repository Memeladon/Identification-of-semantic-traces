from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from .database.config import PONY_ORM_CONFIG
from .database.register import register_pony_orm

from .routing.pages import pageRouter
from .settings import PROJECT_NAME, PROJECT_VERSION



app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

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


# Регистрация Pony ORM
register_pony_orm(app, PONY_ORM_CONFIG, generate_schemas=True)

@app.get("/")
def home():
    return "Hello, World!"

