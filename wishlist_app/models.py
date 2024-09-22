from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from wishlist_app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255))


class Wish(db.Model):
    __tablename__ = 'wishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    uploaded = Column(DateTime, nullable=False, default=func.now())
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String(100), unique=True)
    creator = relationship('User', backref='wishes')