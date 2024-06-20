from fastapi import APIRouter, Depends, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Annotated
from dependencies import User, get_current_user
import os


router = APIRouter(prefix="/api")


@router.get("/files")
async def get_files(user: Annotated[User, Depends(get_current_user)]) -> list[str]:
    filenames = next(os.walk(f"./files/{user.id}"), (None, [], []))[2]
    return filenames


@router.get("/file/{filename}")
async def get_file(filename: str, user: Annotated[User, Depends(get_current_user)]) -> FileResponse:
    file_path = f"./files/{user.id}/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@router.delete("/file/{filename}")
async def delete_file(filename: str, user: Annotated[User, Depends(get_current_user)]):
    file_path = f"./files/{user.id}/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    os.remove(file_path)


@router.post("/file", status_code=201)
async def upload_file(file: UploadFile, user: Annotated[User, Depends(get_current_user)]):
    if not os.path.exists(f"./files/{user.id}"):
        os.mkdir(f"./files/{user.id}")
    content = await file.read()
    with open(f"./files/{user.id}/{file.filename}", "wb") as f:
        f.write(content)
