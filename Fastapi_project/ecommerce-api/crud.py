from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from models import Product, Category, Order, User
from schemas import ProductCreate, CategoryCreate, OrderCreate, UserCreate
from auth import get_password_hash

# CRUD Operations or Categories
async def create_category(db: AsyncSession, category: CategoryCreate):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category).options(selectinload(Category.products)))
    return result.scalars().all()

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()

async def update_category(db: AsyncSession, category_id: int, category: CategoryCreate):
    existing_category = await get_category(db, category_id)
    if not existing_category:
        raise HTTPException(f"Category with id {category_id} does not exist.")
    
    existing_category.name = category.name
    await db.commit()
    await db.refresh(existing_category)
    return existing_category

async def delete_category(db: AsyncSession, category_id: int):
    category = await get_category(db, category_id)
    if category:
        await db.delete(category)
        await db.commit()
        return category
    return None

# CRUD Operations for Products
async def create_product(db: AsyncSession, product: ProductCreate):
    new_product = Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product).options(selectinload(Product.category)))
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id).options(joinedload(Product.category)))
    return result.scalar_one_or_none()

async def update_product(db: AsyncSession, product_id: int, product: ProductCreate):
    existing_product = await get_product(db, product_id)
    if not existing_product:
        raise HTTPException(f"Product with id {product_id} does not exist.")
    
    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.category_id = product.category_id
    
    await db.commit()
    await db.refresh(existing_product)
    return existing_product

async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    if product:
        await db.delete(product)
        await db.commit()
        return product
    return None

# CRUD Operations for Orders

async def create_order(db: AsyncSession, order: OrderCreate):
    new_order = Order(**order.model_dump())
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def update_order(db: AsyncSession, order_id: int, order: OrderCreate):
    existing_order = await get_order(db, order_id)
    if not existing_order:
        raise HTTPException(f"Order with id {order_id} does not exist.")
    
    existing_order.product_id = order.product_id
    existing_order.quantity = order.quantity
    existing_order.total = order.total
    existing_order.email = order.email

    await db.commit()
    await db.refresh(existing_order)
    return existing_order

async def delete_order(db: AsyncSession, order_id: int):
    order = await get_order(db, order_id)
    if order:
        await db.delete(order)
        await db.commit()
        return order
    return None


# CRUD Operations for Users

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def delete_user(db: AsyncSession, email: str):
    user = await get_user_by_email(db, email)
    if user:
        await db.delete(user)
        await db.commit()
        return user
    return None





