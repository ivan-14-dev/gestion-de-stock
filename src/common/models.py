from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Category:
    id: int
    name: str
    parent_id: Optional[int] = None

@dataclass
class Supplier:
    id: int
    name: str
    contact: str = ""
    email: str = ""
    phone: str = ""

@dataclass
class Variant:
    size: str
    color: str
    quantity: int
    sku: str = ""

@dataclass
class Product:
    id: int
    reference: str
    name: str
    category_id: int
    supplier_id: int
    price: float
    variants: List[Variant] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    barcode: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Movement:
    id: int
    product_id: int
    type: str  # 'in', 'out', 'adjustment'
    quantity: int
    reason: str = ""
    user: str = ""
    date: datetime = field(default_factory=datetime.now)

# Global data stores
categories: List[Category] = []
suppliers: List[Supplier] = []
products: List[Product] = []
movements: List[Movement] = []