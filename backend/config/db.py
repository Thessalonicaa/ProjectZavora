from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():
    try:
        connect(
            db=os.getenv('MONGO_DB'),
            host=os.getenv('MONGO_URI'),
            username=os.getenv('MONGO_USER'),
            password=os.getenv('MONGO_PASS')
        )
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
