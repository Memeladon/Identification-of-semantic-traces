from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from starlette.requests import Request

pageRouter = APIRouter(
    prefix='/iost',
    tags=['IoST'],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory='./staticfiles/templates')


@pageRouter.get('/')
def get_main_page(request: Request):
    return templates.TemplateResponse("mainpage.html", {'request': request})


@pageRouter.get('/login')
def get_main_page(request: Request):
    return templates.TemplateResponse("login.html", {'request': request})

