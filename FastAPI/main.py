import random
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "postgresql+psycopg2://{{sensitive data}}:{{sensitive data}}@postgres_db/postgres?client_encoding=LATIN1"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    expiration_date = Column(String)
    name = Column(String, index=True)
    type = Column(String, index=True)
    opened = Column(Boolean, default=False)

def update_expiration_date(self):
    if self.opened:
        self.expiration_date = "5"



Base.metadata.create_all(bind=engine)


app = FastAPI()



class ProductCreate(BaseModel):
    id: int
    expiration_date: str
    name: str
    type: str
    opened: bool



class ProductResponse(BaseModel):
    id: int
    expiration_date: str
    name: str
    type: str
    opened: bool


    class Config:
        orm_mode = True



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/products/opened/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.opened = True
    product.expiration_date = "5"
    db.commit()
    return product

@app.post("/products", response_model=ProductResponse)
def create_product(expiration_date: str, name: str, type: str):
    db:Session = SessionLocal()
    new_product = Product(id = random.randint(0,1000000000), expiration_date=expiration_date, name=name, type=type)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/products/all", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

