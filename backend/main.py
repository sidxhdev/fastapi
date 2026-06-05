from fastapi import FastAPI

from .models import Product


app = FastAPI()

@app.get("/")
def greet():
    return "welcome to fastapi"

products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    Product(id=2, name="laptop", description="gaming laptop", price=999, quantity=6),
    Product(id=3, name="pen", description="ball pen", price=99, quantity=10),
    Product(id=4, name="book", description="100 pages", price=199, quantity=6)
]
@app.get("/products")
def get_all_products():
    return products

@app.get("/product/{id}")
def get_all_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
        

    return "product not found"    

@app.post("/product")
def add_product(product: Product):
    products.append(product)
    return product

@app.delete("/product")
def delete_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
        

    return "product not found" 