from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.requests import Request

pageRouter = APIRouter(
    # prefix='/weather',
    tags=['IoST'],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory='./internal/templates')


@pageRouter.get('/')
def get_main_page(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})


@pageRouter.get('/login')
def get_main_page(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})
