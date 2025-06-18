from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, ForeignKey
from database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete", lazy = "selectin")

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products", lazy = "selectin")
    orders = relationship("Order", back_populates="product", lazy = "selectin")


class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)
    email : Mapped[str] = mapped_column(String, unique=True, nullable=False)

    product = relationship("Product", back_populates="orders", lazy = "selectin")


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)