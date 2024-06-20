from fastapi import APIRouter, Request, Depends
from typing import Annotated
from dependencies import get_current_user
from routers.files import get_files
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    default_response_class=HTMLResponse
)

templates = Jinja2Templates(directory="templates")


@router.get('/')
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@router.get('/files')
async def files_page(request: Request, files: Annotated[list[str], Depends(get_files)]):
    return templates.TemplateResponse(request=request, name='files.html', context={'files': files})


@router.get('/profile', dependencies=[Depends(get_current_user)])
async def profile_page(request: Request):
    return templates.TemplateResponse(request=request, name='profile.html')
