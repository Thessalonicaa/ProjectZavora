from mongoengine import Document, StringField, IntField, FloatField, ListField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime

class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    email = StringField()
    role = StringField(default='user')
    is_seller = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    profile_image = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['username', 'email']
    }

class Seller(Document):
    user = ReferenceField('User', required=True, unique=True)
    username = StringField(required=True, unique=True)
    business_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    phonenumber = StringField()
    contact_info = StringField()
    description = StringField()
    role = StringField(default='Seller')  # ← ADD THIS LINE
    is_active = BooleanField(default=True)  # ← ADD THIS LINE
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'sellers',
        'indexes': ['user', 'username', 'email']
    }
    

class Car(Document):
    seller = ReferenceField(Seller, required=True)
    brand = StringField(required=True)
    model = StringField(required=True)
    year = IntField(required=True)
    license_plate = StringField()
    description = StringField()
    price = FloatField(required=True)
    images = ListField(StringField())
    
    fuel_type = StringField(default='Petrol', choices=['Petrol', 'Diesel', 'Hybrid', 'Electric'])
    transmission = StringField(default='Automatic', choices=['Automatic', 'Manual'])
    car_type = StringField(default='Sedan', choices=['Sedan', 'SUV', 'Pickup', 'Van', 'Sports'])
    
    sold_out = BooleanField(default=False)
    views = IntField(default=0)
    video_url = StringField()
    
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'cars',
        'indexes': ['seller', 'brand', 'created_at']
    }

class Conversation(Document):
    participants = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'conversations'
    }

class Message(Document):
    conversation = ReferenceField(Conversation, required=True)
    sender = StringField(required=True)
    content = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'messages',
        'indexes': ['conversation', 'created_at']
    }