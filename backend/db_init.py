from pymongo import MongoClient
import os

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://loeitech_admin:G7%23u4sK!8zWb@202.29.231.188:27018/ZAVORA?authSource=admin')

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.admin.command('ping')
    print("✓ MongoDB connected successfully")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    raise

db = client['ZAVORA']

# Export for use in other modules
__all__ = ['db', 'client']
