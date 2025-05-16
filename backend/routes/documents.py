from fastapi import APIRouter, Depends, Form, Path, UploadFile, File, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import Tag, User, Document as DocModel
from database import get_db
from auth import fastapi_users
from config import settings
import os
import json
import openai
from uuid import UUID
from fastapi import BackgroundTasks, Response
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from fastapi.responses import JSONResponse , FileResponse
from docx import Document
from auxiliars import *
from config import settings 

router = APIRouter(prefix="/documents", tags=["documents"])


info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", settings.B2_KEY_ID, settings.B2_APP_KEY)
bucket = b2_api.get_bucket_by_name(settings.BUCKET_NAME)
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)



@router.get("/")
async def get_document(current_user: User = Depends(fastapi_users.current_user()) , 
    db: AsyncSession = Depends(get_db) ):

    result = await db.execute(select(DocModel).where(DocModel.user_id == current_user.id))
    print("In get_document")
    return {"documents": result.scalars().all()}



@router.delete("/{id}")
async def delete_document(id: UUID = Path(...), current_user: User = Depends(fastapi_users.current_user()) , 
    db: AsyncSession = Depends(get_db) ):
    print("Here deleting documents")
    result = await db.execute(select(DocModel).where(DocModel.id == id))
    document = result.scalars().first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    await db.delete(document)
    await db.commit()

    return {"message": f"Document {id} deleted successfully"}



def upload_to_b2(local_file_path, remote_file_name):
    print(f" Attempting to upload: {local_file_path} as {remote_file_name}...")

    if not os.path.exists(local_file_path):
        print(f" File not found: {local_file_path}")
        return "Error: Local file does not exist"

    try:
        uploaded_file = bucket.upload_local_file(
            local_file=local_file_path, 
            file_name=remote_file_name
        )
        print(f" File uploaded successfully: {uploaded_file.file_name}")
        return f"File uploaded successfully: {uploaded_file.file_name}"

    except Exception as e:
        print(f" Upload failed: {str(e)}")
        return f"Error uploading file: {str(e)}"


@router.post("/")
async def create_document(
    file: UploadFile = File(...),
    name: str = Form(...),
    current_user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db)
):

    print("Here")
    try:
        
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        remote_file_name = f"{current_user.id}_{name}"

        upload_to_b2(temp_file_path, remote_file_name)

        os.remove(temp_file_path)

        
        new_document = DocModel(user_id=current_user.id, name=name, file_path=f"{current_user.id}_{name}") 
        db.add(new_document)
        await db.commit()
        await db.refresh(new_document)
        print(f"Document created in DB with ID: {new_document.id}")

    except Exception as e:
        print(f"Database commit failed: {e}")
        await db.rollback()
        return {"error": "Failed to store document in DB"}

    return {"message": "New document created successfully"}

@router.get("/{document_id}")
async def get_document(document_id: UUID, background_tasks: BackgroundTasks, 
     current_user: User = Depends(fastapi_users.current_user()), 
     db: AsyncSession = Depends(get_db)):

    print(f" Received request to fetch document: {document_id}")

    
    document = await db.get(DocModel, str(document_id))
    if not document:
        print(f" Document {document_id} not found in database.")
        raise HTTPException(status_code=404, detail="Document not found")

    file_name = document.file_path  
    print(f" Found document in DB: {file_name}")

    local_file_path = f"temp_{file_name}"
    print(f" Temporary local file path: {local_file_path}")

    try:
       
        print(f"⬇ Downloading {file_name} from Backblaze B2...")
        downloaded_file = bucket.download_file_by_name(file_name)
        downloaded_file.save_to(local_file_path)
        print(f" Download complete: {local_file_path}")

        
        if not os.path.exists(local_file_path):
            print(f" Error: The file {local_file_path} was not found after downloading!")
            raise HTTPException(status_code=500, detail="Downloaded file is missing!")
        
        
        background_tasks.add_task(os.remove, local_file_path)
        print(f" File scheduled for cleanup after response: {local_file_path}")

        
        headers = {
            "Content-Disposition": f'attachment; filename="{os.path.basename(file_name)}"'
        }

        print(f" Sending file with Content-Disposition: {headers['Content-Disposition']}")

        return FileResponse(
            local_file_path, 
            filename=os.path.basename(file_name), 
            media_type="application/octet-stream",
            headers=headers
        )

    except Exception as e:
        print(f" Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")
    
    
@router.get("/back/{document_id}")
async def get_modified_document(
    document_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db)
):
    print(f"Received request to fetch and modify document: {document_id}")

    document = await db.get(DocModel, str(document_id))
    if not document:
        print(f"Document {document_id} not found in database.")
        raise HTTPException(status_code=404, detail="Document not found")

    file_name = document.file_path
    print(f"Found document in DB: {file_name}")

    local_file_path = os.path.join(TEMP_DIR, f"temp_{file_name}")
    print(f"Temporary local file path: {local_file_path}")

    try:
        print(f"Downloading {file_name} from Backblaze B2...")
        downloaded_file = bucket.download_file_by_name(file_name)
        downloaded_file.save_to(local_file_path)
        print(f"Download complete: {local_file_path}")

        if not os.path.exists(local_file_path):
            print(f"Error: The file {local_file_path} was not found after downloading!")
            raise HTTPException(status_code=500, detail="Downloaded file is missing!")

        result = await db.execute(select(Tag).where(Tag.user_id == current_user.id))
        tags = result.scalars().all()

        doc = Document(local_file_path)
        
        variable_dict = {}
        for tag in tags:
            if tag.tag_type == "image":
                variable_dict[tag.tag_name] = tag.image_url
            else:
                variable_dict[tag.tag_name] = tag.tag_fill

        replace_variables_in_doc(doc, variable_dict)
        
        modified_file = BytesIO()
        doc.save(modified_file)
        modified_file.seek(0)

        modified_filename = f"modified-{os.path.basename(file_name)}"
        modified_path = os.path.join(TEMP_DIR, modified_filename)

        with open(modified_path, "wb") as temp_file:
            temp_file.write(modified_file.read())
        modified_file.seek(0)

        background_tasks.add_task(os.remove, local_file_path)
        background_tasks.add_task(os.remove, modified_path)

        headers = {
            "Content-Disposition": f'attachment; filename="{modified_filename}"'
        }
        print(f"Sending modified file: {modified_filename}")

        return FileResponse(
            modified_path,
            filename=modified_filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers=headers
        )

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
