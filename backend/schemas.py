from pydantic import BaseModel, field_validator


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    @field_validator("name", "description")
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("cannot be empty")
        return v.strip()

    @field_validator("price")
    @classmethod
    def price_non_negative(cls, v):
        if v < 0:
            raise ValueError("price cannot be negative")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_non_negative(cls, v):
        if v < 0:
            raise ValueError("quantity cannot be negative")
        return v


class ProductCreate(ProductBase):
    id: int

    @field_validator("id")
    @classmethod
    def id_positive(cls, v):
        if v <= 0:
            raise ValueError("id must be greater than 0")
        return v


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True