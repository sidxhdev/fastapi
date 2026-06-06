import os
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv(".env.local")
from .database import engine, get_db
from .models import Product
from .schemas import ProductCreate, ProductUpdate, ProductResponse

import logging

logger = logging.getLogger(__name__)

# Create tables
Product.__table__.create(engine, checkfirst=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No products available")
    return products

@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
    return product

@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    if product_data.id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    if not product_data.name or not product_data.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product name cannot be empty")
    if product_data.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product price cannot be negative")
    if product_data.quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product quantity cannot be negative")
    
    existing = db.query(Product).filter(Product.id == product_data.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product with ID {product_data.id} already exists")
    
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    if not product_data.name or not product_data.name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product name cannot be empty")
    if product_data.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product price cannot be negative")
    if product_data.quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product quantity cannot be negative")
    
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
    
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{id}", status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product removed successfully", "product": ProductResponse.from_orm(product).dict()}
