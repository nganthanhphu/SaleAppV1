import json
from base64 import encode

from saleapp import app, db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as RoleEnum
from flask_login import UserMixin
import hashlib

class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), unique=True, nullable=False)
    active = Column(Boolean, default =True)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name

class User(BaseModel, UserMixin):
    email = Column(String(150), unique=True)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)
    avatar = Column(String(150), default="https://img.freepik.com/free-vector/user-circles-set_78370-4704.jpg")
    role = Column(Enum(UserRole), default=UserRole.USER)

class Category(BaseModel):
    products = relationship('Product', backref='category', lazy=True)

class Product(BaseModel):
    price = Column(Float, default=0.0)
    image = Column(String(300), default="https://dlcdnwebimgs.asus.com/gain/859297d3-da9f-4807-81e8-7a2fdf14204d/")
    cate_id = Column(Integer, ForeignKey(Category.id), nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        c1 = Category(name='Laptop')
        c2 = Category(name='Mobile')
        c3 = Category(name='Tablet')

        db.session.add_all([c1,c2,c3])

        with open("data/product.json", encoding="utf-8") as f:
            products = json.load(f)

            for p in products:
                db.session.add(Product(**p))
        pwd = hashlib.md5('123'.encode('utf-8')).hexdigest()
        u1 = User(name='User', username='user', password=pwd)
        db.session.add(u1)
        db.session.commit()