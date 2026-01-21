from datetime import timedelta
import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    
    if MONGO_URI:
        MONGODB_SETTINGS = {
            'host': MONGO_URI
        }
    else:
        MONGODB_SETTINGS = {
            'db': 'ZAVORA',
            'host': 'mongodb://loeitech_admin:G7%23u4sK!8zWb@202.29.231.188:27018/ZAVORA?authSource=admin'
        }
    JWT_SECRET_KEY = "Zavora_8f3c9a2e6b7d4f1cA9E2D5K7M4R8Q6W"  # ต้องเปลี่ยนเป็น key ที่ปลอดภัย
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)