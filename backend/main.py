from fastapi import FastAPI, Depends,  Form, File, UploadFile, Path, HTTPException
from fastapi.responses import JSONResponse , FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from database import database, engine, Base, get_db
from models import User, Tag, Document as DocModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from docx import Document
from io import BytesIO
from uuid import UUID
from fastapi import BackgroundTasks, Response
from routes.tags import router as tags_router
from routes.documents import router as documents_router
import os
import re
from auxiliars import *
from auth import fastapi_users, auth_backend, BaseUser, BaseUserCreate, UserRead, BaseUserUpdate



origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
]



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(fastapi_users.get_auth_router(auth_backend),prefix="/auth/jwt",tags=["auth"],)
app.include_router(fastapi_users.get_register_router(BaseUser, BaseUserCreate),prefix="/auth",tags=["auth"],)
app.include_router(fastapi_users.get_users_router(UserRead, BaseUserUpdate),prefix="/users",tags=["users"],)
app.include_router(tags_router)
app.include_router(documents_router)



@app.post("/auth/jwt/logout", tags=["auth"], status_code=200)
async def custom_logout():
    """Custom logout response."""
    return JSONResponse(content={"message": "Successfully logged out"}, status_code=200)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        await create_tables()
        print(" Database connected successfully.")
    except Exception as e:
        print(f" Database connection error: {e}")



@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




