from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(sparse=True)  # Optional field, allows null values
    password = StringField(required=True)
    role = StringField(default='user')  # 'user', 'seller', or 'admin'
    is_seller = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    profile_image = StringField()  # Base64 image data
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    reset_token = StringField(max_length=100, default=None, null=True)
    reset_token_expiry = DateTimeField(default=None, null=True)

    meta = {
        'collection': 'users',
        'indexes': ['username']
    }

    def __repr__(self):
        return f'<User {self.username}>'
