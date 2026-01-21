"""
Seller Model - MongoDB/MongoEngine
"""
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime

class Seller(Document):
    """Seller model for business information"""
    user = ReferenceField('User', required=True, unique=True)
    username = StringField(required=True, unique=True)
    business_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    phonenumber = StringField()
    contact_info = StringField()
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'sellers',
        'indexes': ['user', 'username', 'email']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user.id) if self.user else None,
            'username': self.username,
            'business_name': self.business_name,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'contact_info': self.contact_info,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
