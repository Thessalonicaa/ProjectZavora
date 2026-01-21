
"""
Migration script to add sold_out field to all existing cars in MongoDB
Run this once to initialize the field
"""

from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/car_sales')

try:
    client = MongoClient(MONGO_URI)
    db = client['car_sales']
    
    # Add sold_out field to all cars that don't have it
    result = db.cars.update_many(
        {'sold_out': {'$exists': False}},
        {'$set': {'sold_out': False}}
    )
    
    print(f"✓ Migration completed!")
    print(f"  Modified documents: {result.modified_count}")
    print(f"  Total cars in database: {db.cars.count_documents({})}")
    
    # Verify all cars now have sold_out field
    cars_without_field = db.cars.count_documents({'sold_out': {'$exists': False}})
    print(f"  Cars without sold_out field: {cars_without_field}")
    
    if cars_without_field == 0:
        print("✓ All cars have sold_out field!")
    else:
        print(f"⚠ Warning: {cars_without_field} cars still missing sold_out field")
    
    client.close()
    
except Exception as e:
    print(f"✗ Migration error: {e}")
    raise
