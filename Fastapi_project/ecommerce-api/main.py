from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, Base, get_db, AsyncSession
import crud
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models import Product,User
from schemas import (CategoryCreate, CategoryResponse, ProductCreate, ProductResponse,
                      OrderCreate, OrderResponse, UserCreate, UserResponse, Token)
import aiosmtplib
from email.mime.text import MIMEText
import logging
from auth import (create_access_token, get_current_user, get_current_admin, 
                 verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, Role)
from datetime import timedelta
# import ipdb





app = FastAPI(title="E-commerce Product API")


# @app.on_event("startup")
# async def handle_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# Create database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def startup():
    await init_db()

@app.on_event("startup")
async def handle_startup():
    await startup()


#user authentication and authorization end points
@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db, user)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                               db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#category end points
@app.post("/category", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
   
    return await crud.create_category(db, category)

@app.get("/category", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    return await crud.get_categories(db)

@app.get("/category/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    category = await crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/category/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    existing_category = await crud.get_category(db, category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    updated_category = await crud.update_category(db, category_id, category)
    return updated_category


@app.delete("/category/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
   
    category = await crud.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

#product end points

@app.post("/product", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    #set_trace()
    created_product = await crud.create_product(db, product)

    # Reload the product to ensure category is loaded
    db.expunge_all()  # Clear session cache
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).where(Product.id == created_product.id)
    )
    product_with_category = result.scalars().first()

    return product_with_category


@app.get("/product", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
   
    return await crud.get_products(db)

@app.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/product/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    # Fetch the existing product
    existing_product = await crud.get_product(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product using the CRUD function
    updated_product = await crud.update_product(db, product_id, product)

    # Ensure the updated product includes the related category
    result = await db.execute(
        select(Product).options(selectinload(Product.category)).where(Product.id == updated_product.id)
    )
    product_with_category = result.scalars().first()

    return product_with_category


@app.delete("/product/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
   
    product = await crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add email configuration (you should move these to a config file in production)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USER = "heril.btridhyatech@gmail.com"
EMAIL_PASSWORD = "ztjmznbzucwquckg"  # Use app-specific password for Gmail
FROM_EMAIL = "heril.btridhyatech@gmail.com"

# Email sending function
async def send_confirmation_email(order_id: int, product_id: int, quantity: int, total: float, recipient_email: str):
    try:
        message = MIMEText(f"""Thank you for your order!
        
        Order Details:
        Order ID: {order_id}
        Product ID: {product_id}
        Quantity: {quantity}
        Total: ${total:.2f}
        
        We'll notify you when your order ships.""")
        message['Subject'] = f"Order Confirmation - Order #{order_id}"
        message['From'] = FROM_EMAIL
        message['To'] = recipient_email

        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            username=EMAIL_USER,
            password=EMAIL_PASSWORD,
            use_tls=True,
        )
        logger.info(f"Confirmation email sent for order #{order_id}")
    except Exception as e:
        logger.error(f"Failed to send email for order #{order_id}: {str(e)}")

#order end points

@app.post("/order", response_model= OrderResponse)
async def create_order(order: OrderCreate, background_tasks : BackgroundTasks, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    created_order =  await crud.create_order(db, order)

    background_tasks.add_task(
        send_confirmation_email,
        created_order.id,
        created_order.product_id,
        created_order.quantity,
        created_order.total,
        order.email  # Use email from request
    )
    return created_order

@app.get("/order/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    order = await crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/order", response_model=list[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
   
    return await crud.get_orders(db)

@app.put("/order/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    existing_order = await crud.get_order(db, order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = await crud.update_order(db, order_id, order)
    return updated_order

@app.delete("/order/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
   
    order = await crud.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}


#user end points

@app.get("/user", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    return await crud.get_users(db)

@app.delete("/user/{email}")
async def delete_user(email: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_admin)):
    user = await crud.delete_user(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

