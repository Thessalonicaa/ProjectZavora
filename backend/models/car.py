from mongoengine import Document, StringField, IntField, FloatField, ListField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime

__all__ = ['Car']

# Car model

class Car(Document):
    """Car model"""
    
    seller = ReferenceField('Seller', required=True)
    
    # Basic Info
    brand = StringField(required=True)
    model = StringField(required=True)
    color = StringField()
    year = IntField(required=True)
    price = FloatField(required=True)
    
    # Vehicle Type
    vehicle_type = StringField(default='Car')  # Car, Motorcycle, Bike
    
    # Engine & Performance
    fuel_type = StringField()  # Petrol, Diesel, Hybrid, Electric
    transmission = StringField()  # Automatic, Manual, CVT, etc.
    engine_size = StringField()  # 2000cc, 3.5L, etc.
    mileage = IntField(default=0)
    gas_system = StringField(default='None')  # NGV, LPG, None
    drive_system = StringField()  # FWD, RWD, AWD, 4WD
    
    # Car Details
    car_type = StringField()  # Sedan, SUV, Pickup, Van, etc.
    license_plate = StringField()
    description = StringField()
    
    # Dynamic Fields for Specific Car Types
    # MPV
    mpv_size = StringField()  # Compact, Mid-Size, Full-Size
    
    # Convertible
    convertible_top = StringField()  # Soft Top, Retractable Hard Top
    convertible_seats = StringField()  # 2 Seats, 4 Seats
    
    # Van
    van_type = StringField()  # Cargo Van, Minivan
    
    # SUV
    suv_seats = StringField()  # 2 Seats, 4 Seats
    
    # Pickup
    pickup_cab = StringField()  # Single Cab, Extra Cab, Double Cab
    pickup_body_type = StringField()  # Box Body, Flatbed, Dropside
    
    # Media & Status
    images = ListField(StringField(), default=list)
    sold_out = BooleanField(default=False)
    views = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'cars'
    }
