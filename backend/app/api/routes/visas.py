#api for visa requirements of a country

from fastapi import APIRouter

from fastapi import Depends, HTTPException, Request,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.db import get_db
from typing import Annotated
from app.core.models import Country
from app.core.models import Visa

from app.core.schemas import CountryCreate, CountryResponse, VisaCreate, VisaResponse


router = APIRouter()


#get all countries
@router.get(
        "/country", 
        tags=["Country"], 
        response_model=list[CountryResponse])
def get_all_country(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Country))
    countries = result.scalars().all()

    return countries
    
#get country by id
@router.get("/country/{country_id}", tags=["Country"], response_model=CountryResponse)
def get_country_by_id(country_id:int, db: Annotated[Session, Depends(get_db)]):
    country = db.execute(
        select(Country).where(Country.id == country_id)
    )
    country = country.scalars().first()

    if country:
        return country
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Country not found"
    )


#create country
@router.post("/country", tags=["Country"], response_model = CountryResponse)
def create_country(country:CountryCreate, db: Annotated[Session, Depends(get_db)]):
    existing_country = db.execute(select(Country).where(Country.name == country.name))
    existing_country = existing_country.scalars().first()
    if existing_country:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Country already exists"
        )
    
    new_country = Country(
        name= country.name
    )
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country


#get all visa types by country id
@router.get("/country/{country_id}/visas", tags=["Country"], response_model=list[VisaResponse])
def get_visa_by_country_id(country_id:int, db: Annotated[Session, Depends(get_db)]):
    country = db.execute(
        select(Country).where(Country.id == country_id)
    )
    country = country.scalars().first()
    if not country:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Country not found"
        )
    
    visas = country.visas
    return visas

#create visa(with country_id)
@router.post("/country/{country_id}/visa", tags=["Country"], response_model= VisaResponse)
def create_visa(visa: VisaCreate, db:Annotated[Session, Depends(get_db)]):
    country = db.execute(
        select(Country).where(Country.id == visa.country_id)
    )

    country = country.scalars().first()

    if not country:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Country not found"
        )
    
    new_visa = Visa(
        type = visa.type,
        eligibility = visa.eligibility,
        materials = visa.materials,
        country_id = visa.country_id
    )

    db.add(new_visa)
    db.commit()
    db.refresh(new_visa)
    return new_visa