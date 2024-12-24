from fastapi import APIRouter, Depends, HTTPException, Form , UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from app.db.database import get_db
from app.products.models import Product
from app.users.models import User
from app.products.schemas import ProductCreateUpdate, ProductResponse
from app.security import get_current_user, get_admin_user
from typing import Optional
from uuid import uuid4


router = APIRouter()

UPLOAD_DIR = "uploads"

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function to delete an old image
def delete_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)



@router.post("/products", response_model=ProductResponse)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Sauvegarder l'image
    image_filename = f"{uuid4()}_{image.filename}"  # Crée un nom unique pour éviter les conflits
    image_path = os.path.join(UPLOAD_DIR, image_filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Créer le produit
    new_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_path=image_filename,  # Sauvegarder seulement le nom dans la base de données
        user_id=current_user.id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # Retourner la réponse
    return ProductResponse(
        id=new_product.id,
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        category=new_product.category,
        image_path=new_product.image_path,  # Retourner seulement le nom de l'image
        user=current_user.username,
    )


# Update a product
@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Trouver le produit
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the user")

    # Mettre à jour les champs
    product.name = name
    product.description = description
    product.price = price
    product.category = category

    # Gestion de l'image
    if image:
        # Supprimer l'ancienne image
        delete_image(product.image_path)

        # Enregistrer la nouvelle image
        new_image_filename = f"{uuid4()}_{image.filename}"
        new_image_path = os.path.join(UPLOAD_DIR, new_image_filename)
        with open(new_image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Mettre à jour le nom de l'image dans la base de données
        product.image_path = new_image_filename

    db.commit()
    db.refresh(product)
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        image_path=product.image_path,  # Retourner seulement le nom de l'image
        user=current_user.username,
    )

# Get all products by the current user
@router.get("/products/user", response_model=List[ProductResponse])
async def get_user_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    products = db.query(Product).filter(Product.user_id == current_user.id).all()

    
    return [
        ProductResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category,
            image_path=p.image_path,
            user=current_user.username,  
        )
        for p in products
    ]


# Get all products 
@router.get("/products", response_model=List[ProductResponse])
async def get_all_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = db.query(Product).all()
    return [
        ProductResponse(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category,
            image_path=p.image_path,
            user=p.user.username,  
        )
        for p in products
    ]

# Get one product by ID
@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        image_path=product.image_path,
        user=product.user.username,
    )

# Delete a product
@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    
    product = db.query(Product).filter(Product.id == product_id, Product.user_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by the user")

    
    delete_image(product.image_path)

    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}
