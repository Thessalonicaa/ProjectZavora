from datetime import timedelta

class Config:
    MONGODB_SETTINGS = {
        'db': 'MyCarsWed',
        'host': 'localhost',
        'port': 27017
    }
    JWT_SECRET_KEY = "Zavora_8f3c9a2e6b7d4f1cA9E2D5K7M4R8Q6W"  # ต้องเปลี่ยนเป็น key ที่ปลอดภัย
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)