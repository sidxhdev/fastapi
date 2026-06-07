import os
import json
import redis as redis_client

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

Product.__table__.create(engine, checkfirst=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    
allow_origins=[
    "http://localhost:3000",
    "http://fastapi-inventory-frontend.s3-website.ap-south-1.amazonaws.com",
    "https://inventory-manager.sidxh.com",
    
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis setup
r = redis_client.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)
CACHE_TTL = 60  # seconds


def invalidate_cache(product_id: int = None):
    r.delete("products:all")
    if product_id:
        r.delete(f"products:{product_id}")


@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    cached = r.get("products:all")
    if cached:
        return json.loads(cached)
    products = db.query(Product).all()
    r.setex("products:all", CACHE_TTL, json.dumps([ProductResponse.from_orm(p).dict() for p in products]))
    return products


@app.get("/products/{id}", response_model=ProductResponse)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    cached = r.get(f"products:{id}")
    if cached:
        return json.loads(cached)
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
    r.setex(f"products:{id}", CACHE_TTL, json.dumps(ProductResponse.from_orm(product).dict()))
    return product


@app.post("/products/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.id == product_data.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product with ID {product_data.id} already exists")
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    invalidate_cache()
    return product


@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    if id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID must be greater than 0")
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
    for key, value in product_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    invalidate_cache(product_id=id)
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
    invalidate_cache(product_id=id)
    return {"message": "Product removed successfully", "product": ProductResponse.from_orm(product).dict()}