from __future__ import annotations

from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from datetime import UTC,datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped,mapped_column, relationship
from app.core.db import Base  

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,index=True)
    username: Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String(120),unique=True,nullable=False)
    
    applications: Mapped[list[Application]] = relationship(back_populates="applicant")


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country: Mapped[str] = mapped_column(String,nullable=False)
    visa_type: Mapped[str] = mapped_column(String,nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda:datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    applicant: Mapped[User] = relationship(back_populates="applications")
    items: Mapped[list[Item]] = relationship(back_populates="application")

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String,nullable=False)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), nullable=False, index=True)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)

    application: Mapped[Application] = relationship(back_populates="items")

class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String,nullable=False)

    visas: Mapped[list[Visa]] = relationship(back_populates="country")

class Visa(Base):
    __tablename__ = "visas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    visa_type: Mapped[str] = mapped_column(String,nullable=False)
    eligibility: Mapped[list[str]] = mapped_column(ARRAY(String))
    materials: Mapped[list[str]] = mapped_column(ARRAY(String))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), nullable=False, index=True)

    country: Mapped[Country] = relationship(back_populates="visas")