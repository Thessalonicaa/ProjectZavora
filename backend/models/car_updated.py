from datetime import datetime
from database import db

class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.String(24), primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    images = db.Column(db.JSON, default=[])
    license_plate = db.Column(db.String(20), unique=True)
    seller_id = db.Column(db.String(100), nullable=False)
    seller_username = db.Column(db.String(100), nullable=False)
    
    fuel_type = db.Column(db.String(50), default='Petrol')
    transmission = db.Column(db.String(50), default='Automatic')
    car_type = db.Column(db.String(50), default='Sedan')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'description': self.description,
            'images': self.images or [],
            'license_plate': self.license_plate,
            'seller_id': self.seller_id,
            'seller_username': self.seller_username,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'car_type': self.car_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Car {self.brand} {self.model}>'