import json
import os
import pandas as pd
from .models import categories, suppliers, products, movements, Category, Supplier, Product, Movement, Variant
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Firebase initialization (basic setup - replace with actual credentials)
try:
    cred = credentials.Certificate('firebase-service-account.json')  # Place this file in the project root
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://your-project-id.firebaseio.com/'  # Replace with actual URL
    })
    firebase_enabled = True
except Exception as e:
    print(f"Firebase not configured: {e}")
    firebase_enabled = False

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_data():
    ensure_data_dir()
    # Load categories
    cat_file = os.path.join(DATA_DIR, 'categories.json')
    if os.path.exists(cat_file):
        with open(cat_file, 'r') as f:
            data = json.load(f)
            categories.clear()
            for item in data:
                categories.append(Category(**item))

    # Load suppliers
    sup_file = os.path.join(DATA_DIR, 'suppliers.json')
    if os.path.exists(sup_file):
        with open(sup_file, 'r') as f:
            data = json.load(f)
            suppliers.clear()
            for item in data:
                suppliers.append(Supplier(**item))

    # Load products
    prod_file = os.path.join(DATA_DIR, 'products.json')
    if os.path.exists(prod_file):
        with open(prod_file, 'r') as f:
            data = json.load(f)
            products.clear()
            for item in data:
                item['created_at'] = datetime.fromisoformat(item['created_at'])
                item['updated_at'] = datetime.fromisoformat(item['updated_at'])
                item['variants'] = [Variant(**v) for v in item['variants']]
                products.append(Product(**item))

    # Load movements
    mov_file = os.path.join(DATA_DIR, 'movements.json')
    if os.path.exists(mov_file):
        with open(mov_file, 'r') as f:
            data = json.load(f)
            movements.clear()
            for item in data:
                item['date'] = datetime.fromisoformat(item['date'])
                movements.append(Movement(**item))

def upload_to_firebase():
   if not firebase_enabled:
       return
   try:
       data = {
           'categories': [cat.__dict__ for cat in categories],
           'suppliers': [sup.__dict__ for sup in suppliers],
           'products': [prod.__dict__ for prod in products],
           'movements': [mov.__dict__ for mov in movements]
       }
       ref = db.reference('/')
       ref.set(data)
       print("Data uploaded to Firebase successfully")
   except Exception as e:
       print(f"Failed to upload to Firebase: {e}")

def save_data():
    ensure_data_dir()
    # Save categories
    cat_file = os.path.join(DATA_DIR, 'categories.json')
    with open(cat_file, 'w') as f:
        json.dump([cat.__dict__ for cat in categories], f, indent=4)

    # Save suppliers
    sup_file = os.path.join(DATA_DIR, 'suppliers.json')
    with open(sup_file, 'w') as f:
        json.dump([sup.__dict__ for sup in suppliers], f, indent=4)

    # Save products
    prod_file = os.path.join(DATA_DIR, 'products.json')
    with open(prod_file, 'w') as f:
        data = []
        for prod in products:
            d = prod.__dict__.copy()
            d['created_at'] = d['created_at'].isoformat()
            d['updated_at'] = d['updated_at'].isoformat()
            d['variants'] = [v.__dict__ for v in d['variants']]
            data.append(d)
        json.dump(data, f, indent=4)

    upload_to_firebase()

    # Save movements
    mov_file = os.path.join(DATA_DIR, 'movements.json')
    with open(mov_file, 'w') as f:
        data = []
        for mov in movements:
            d = mov.__dict__.copy()
            d['date'] = d['date'].isoformat()
            data.append(d)
        json.dump(data, f, indent=4)

def export_csv(filename, data_type):
    ensure_data_dir()
    if data_type == 'products':
        df = pd.DataFrame([{
            'id': p.id,
            'reference': p.reference,
            'name': p.name,
            'category_id': p.category_id,
            'supplier_id': p.supplier_id,
            'price': p.price,
            'variants': json.dumps([v.__dict__ for v in p.variants]),
            'photos': json.dumps(p.photos),
            'barcode': p.barcode,
            'description': p.description
        } for p in products])
    elif data_type == 'categories':
        df = pd.DataFrame([c.__dict__ for c in categories])
    elif data_type == 'suppliers':
        df = pd.DataFrame([s.__dict__ for s in suppliers])
    elif data_type == 'movements':
        df = pd.DataFrame([m.__dict__ for m in movements])
    else:
        return
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)

def import_csv(filename, data_type):
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        return
    df = pd.read_csv(file_path)
    if data_type == 'products':
        for _, row in df.iterrows():
            variants = json.loads(row['variants']) if pd.notna(row['variants']) else []
            photos = json.loads(row['photos']) if pd.notna(row['photos']) else []
            prod = Product(
                id=int(row['id']),
                reference=row['reference'],
                name=row['name'],
                category_id=int(row['category_id']),
                supplier_id=int(row['supplier_id']),
                price=float(row['price']),
                variants=[Variant(**v) for v in variants],
                photos=photos,
                barcode=row['barcode'] if pd.notna(row['barcode']) else '',
                description=row['description'] if pd.notna(row['description']) else ''
            )
            products.append(prod)
    # Add for others if needed