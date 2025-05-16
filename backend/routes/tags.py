from fastapi import APIRouter, Depends, Form, Path, UploadFile, File, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models import Tag, User
from database import get_db
from auth import fastapi_users
from config import settings
import os
import json
import openai
import schemas 
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from uuid import uuid4
from uuid import UUID

from config import settings 
router = APIRouter(prefix="/tags", tags=["tags"])

TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

key=settings.OPENAI_API_KEY


info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", settings.B2_KEY_ID, settings.B2_APP_KEY)
bucket = b2_api.get_bucket_by_name(settings.BUCKET_NAME)


@router.get("/me", response_model=list[dict])
async def get_my_tags(
    current_user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db),
):
    """Get tags for the currently logged-in user"""
    result = await db.execute(select(Tag).filter(Tag.user_id == current_user.id).order_by(Tag.tag_name.asc()))
    tags = result.scalars().all()
    
    return [{"id": tag.id, "name": tag.tag_name, "value": tag.tag_fill, 
             "description":tag.tag_description, "created_at":tag.created_at} for tag in tags]



@router.post("/")
async def create_tag(
    tag_data: schemas.TagCreate,
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(fastapi_users.current_user()) 
):
    
    db_tag = Tag(user_id=current_user.id, tag_name=tag_data.name, tag_fill=tag_data.value, tag_description=tag_data.description)
    try:
        db.add(db_tag) 
        await db.commit()
        await db.refresh(db_tag)

        return {
            "message": "Tag created",
            "tag": {"id": db_tag.id, "name": db_tag.tag_name, "value": db_tag.tag_fill}
        }
    
    except IntegrityError:
        await db.rollback() 
        raise HTTPException(status_code=400, detail="Tag name already exists")

@router.put("/{tag_id}")
async def update_tag(
    tag_data: schemas.TagUpdate,
    tag_id: int = Path(..., title="The ID of the tag to update"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(fastapi_users.current_user()) 
):
    tag = await db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    if tag.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this tag")

    
    tag.tag_name = tag_data.name
    tag.tag_fill = tag_data.value
    tag.tag_description = tag_data.description

    await db.commit()
    await db.refresh(tag)

    return {
        "message": "Tag updated",
        "tag": {"id": tag.id, "name": tag.tag_name, "value": tag.tag_fill, "description": tag.tag_description}
    }

@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(fastapi_users.current_user())
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found or unauthorized")

    await db.delete(tag)
    await db.commit()

    return {"message": f"Tag with ID {tag_id} deleted"}



@router.post("/generate-content")
async def get_ai_content(
    prompt: schemas.PromptBase,
    current_user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_db),
):
    prompt_for_ai = prompt.prompt
    
    client = openai.OpenAI(api_key=key)
    response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": 
                         "Only respond with the content requested. No explanations, no introductions. Be direct."},
                {"role": "user", "content": prompt_for_ai}
            ],
            temperature=0.7,
            top_p=1,
            max_tokens=150
        )
    generated_text = response.choices[0].message.content.strip()
    
    return {"data": generated_text}



def generate_image_filename(user_id: UUID, tag_name: str, ext: str):
    safe_tag = tag_name.lower().replace(" ", "_")
    return f"{user_id}_{safe_tag}.{ext}"

def upload_image_to_b2(file: UploadFile, user_id: UUID, tag_name: str) :
    ext = file.filename.split('.')[-1].lower()
    filename = generate_image_filename(user_id, tag_name, ext)
    b2_key = f"tags/{filename}"

    file_bytes = file.file.read()
    content_type = file.content_type or "application/octet-stream"

    bucket.upload_bytes(file_bytes, b2_key, content_type)

    return b2_key  

@router.post("/image")
async def create_image_tag(
    name: str = Form(...),
    description: str = Form(None),
    category: str = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(fastapi_users.current_user())
):
    image_key = upload_image_to_b2(file, user.id, name)

    tag = Tag(
        user_id=user.id,
        tag_name=name,
        tag_description=description,
        tag_type="image",
        image_url=image_key, 
        tag_fill="",
        category=category,
    )

    db.add(tag)
    await db.commit()
    await db.refresh(tag)

    return tag