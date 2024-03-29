import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routing.pages import pageRouter
from settings import PROJECT_NAME, PROJECT_VERSION

app = FastAPI(title=PROJECT_NAME, version=PROJECT_VERSION)

# ------------ Routing ------------ #
app.mount("/staticfiles", StaticFiles(directory="./staticfiles"), name="staticfiles")
app.include_router(pageRouter)


# host=x.x.x.x:port
if __name__ == "__main__":
    uvicorn.run("srv:app", host="127.0.0.1", port=8000, reload=True)
