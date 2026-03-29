#define shape of input or output (return value)
#schema is for app interaction, models is for db interaction
from __future__ import annotations
from pydantic import BaseModel,ConfigDict,Field, EmailStr
from datetime import datetime
class UserBase(BaseModel):
    username:str = Field(min_length=1,max_length=50)
    email: EmailStr = Field(max_length=120)
    

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True) 
    #allow using dot notation on db object (eg. user.name)

    id:int
    username:str

class UserUpdate(UserBase):
    username: Optional[str] = Field(min_length=1,max_length=50)
    email: Optional[EmailStr] = Field(max_length=120)

#application schema

class ApplicationBase(BaseModel):
    country: str
    visa_type: str

class ApplicationCreate(ApplicationBase):
    user_id: int #TEMPORARY
    country: str
    visa_type: str

class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id:int
    user_id: int
    date_created: datetime
    country: str
    visa_type: str
    applicant: UserResponse
    items: list[ItemResponse]

#item schema
class ItemBase(BaseModel):
    name: str

class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    application_id: int
    is_done: bool

#embassy schema
class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class CountryResponse(CountryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    visas: list[VisaResponse]

#visa schema
class VisaBase(BaseModel):
    visa_type: str
    eligibility: list[str]
    materials: list[str]

class VisaCreate(VisaBase):
    country_id: int

class VisaResponse(VisaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    country_id:int
    country: CountryResponse