from fastapi import APIRouter
from app.core.schemas import ApplicationResponse,ApplicationCreate, ItemResponse
from app.core.models import Application,User, Country, Visa, Item
from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from typing import Annotated

router = APIRouter()

#get application by id
@router.get("/application/{application_id}", tags=["Application"], response_model=ApplicationResponse)
def get_application(application_id:int, db: Annotated[Session, Depends(get_db)]):
    application = db.execute(
        select(Application).where(Application.id == application_id)
    )
    application = application.scalars().first()

    if application:
        return application
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Application not found"
    )


#get all applications of a user
@router.get("/user/{user_id}/applications", tags=["Application"], response_model=list[ApplicationResponse])
def get_user_applications(user_id:int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(
        select(User).where(User.id == user_id)
    )
    user = user.scalars().first()
    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    
    applications = db.execute(
        select(Application).where(Application.user_id == user_id)
    )
    applications = applications.scalars().all()
    return applications

#get all items of an application
@router.get("/application/{application_id}/items", tags=["Item"], response_model=list[ItemResponse])
def get_application_items(application_id:int, db: Annotated[Session, Depends(get_db)]):
    application = db.execute(
        select(Application).where(Application.id == application_id)
    )
    application = application.scalars().first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application.items

#create application (with user_id)
@router.post("/application", tags=["Application"], response_model= ApplicationResponse)
def create_application(application: ApplicationCreate, db:Annotated[Session, Depends(get_db)]):
    #check if user exists
    user = db.execute(
        select(User).where(User.id == application.user_id)
    )

    user = user.scalars().first()

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
        )

    #get visa matching the country name and visa type to retrieve its materials
    visa = db.execute(
        select(Visa)
        .join(Visa.country)
        .filter(Country.name == application.country)
        .filter(Visa.visa_type == application.visa_type)
    ).scalars().first()

    if not visa or not visa.materials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No materials found for the specified country and visa type"
        )
    
    #create new application
    new_application = Application(
        country_id=application.country_id,
        content=application.content,
        user_id=application.user_id,
        visa_id=application.visa_id
    )

    #assign items via relationship so SQLAlchemy handles the FK after INSERT
    new_application.items = [Item(name=material) for material in visa.materials]

    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application