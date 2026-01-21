from datetime import timedelta

class Config:
    MONGODB_SETTINGS = {
        'db': 'MyCarsWed',
        'host': 'localhost',
        'port': 27017
    }
    JWT_SECRET_KEY = "your-secret-key"  # ต้องเปลี่ยนเป็น key ที่ปลอดภัย
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)