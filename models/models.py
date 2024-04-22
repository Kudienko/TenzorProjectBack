from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    city = Column(String)


class Clothes(Base):
    __tablename__ = 'clothes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Integer, ForeignKey("cloth_types.id"), nullable=False)
    weather = Column(Integer, ForeignKey("weather.id"), nullable=False)


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class ClothType(Base):
    __tablename__ = 'cloth_types'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, unique=True)