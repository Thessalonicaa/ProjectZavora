from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

cars_bp = Blueprint('cars', __name__)


#  POST A NEW CAR
@cars_bp.route('/cars', methods=['POST'])
@jwt_required()
def post_car():
    """Post a new car for sale"""
    try:
        identity = get_jwt_identity()
        from models import User, Seller
        from models.car import Car

        user = User.objects(id=identity).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 401

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({'success': False, 'message': 'User is not registered as a seller'}), 403

        data = request.get_json() or {}

        required_fields = ['brand', 'model', 'year', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400

        car = Car(
            seller=seller,
            vehicle_type=data.get('vehicle_type', 'Car'),
            brand=data.get('brand'),
            model=data.get('model'),
            color=data.get('color', ''),
            year=int(data.get('year')),
            price=float(data.get('price', 0)),
            license_plate=data.get('licensePlate', ''),
            description=data.get('description', ''),
            fuel_type=data.get('fuel_type', ''),
            transmission=data.get('transmission', ''),
            car_type=data.get('car_type', ''),
            mileage=int(data.get('mileage', 0)) if data.get('mileage') else 0,
            gas_system=data.get('gas_system', 'None'),
            engine_size=data.get('engine_size', '') or data.get('engineSize', ''),
            drive_system=data.get('drive_system', ''),
            # MPV Options
            mpv_size=data.get('mpv_size', ''),
            # Convertible Options
            convertible_top=data.get('convertible_top', ''),
            convertible_seats=data.get('convertible_seats', ''),
            # Van Options
            van_type=data.get('van_type', ''),
            # SUV Options
            suv_seats=data.get('suv_seats', ''),
            # Pickup Options
            pickup_cab=data.get('pickup_cab', ''),
            pickup_body_type=data.get('pickup_body_type', ''),
            images=data.get('images', [])
        )
        car.save()

        return jsonify({
            'success': True,
            'message': 'Car posted successfully',
            'car_id': str(car.id)
        }), 201

    except Exception as e:
        print(f"Post car error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET ALL CARS (or filter by seller_id)
@cars_bp.route('/cars/my-listings', methods=['GET'])
@jwt_required()
def get_my_listings():
    """Get current seller's car listings"""
    try:
        identity = get_jwt_identity()
        from models import User, Seller
        from models.car import Car

        user = User.objects(id=identity).first()
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 401

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({'success': False, 'message': 'User is not a seller'}), 403

        # Get only this seller's cars
        cars = Car.objects(seller=seller)
        
        cars_list = []
        for car in cars:
            cars_list.append({
                'id': str(car.id),
                '_id': str(car.id),
                'brand': car.brand,
                'model': car.model,
                'color': getattr(car, 'color', ''),
                'year': car.year,
                'price': float(car.price),
                'fuel_type': car.fuel_type,
                'transmission': car.transmission,
                'car_type': car.car_type,
                'engine_size': getattr(car, 'engine_size', ''),
                'description': car.description,
                'images': car.images or [],
                'license_plate': car.license_plate,
                'vehicle_type': getattr(car, 'vehicle_type', 'Car'),
                'mileage': getattr(car, 'mileage', 0),
                'gas_system': getattr(car, 'gas_system', ''),
                'sold_out': getattr(car, 'sold_out', False),
                'views': getattr(car, 'views', 0),
                'created_at': car.created_at.isoformat() if hasattr(car, 'created_at') else None,
                'seller': {
                    'id': str(car.seller.id),
                    'username': car.seller.username,
                    'business_name': car.seller.business_name,
                    'email': car.seller.email,
                    'phonenumber': car.seller.phonenumber,
                    'contact_info': car.seller.contact_info
                } if car.seller else None
            })
        
        return jsonify({
            'success': True,
            'cars': cars_list,
            'total': len(cars_list)
        }), 200

    except Exception as e:
        print(f"Get my listings error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET ALL CARS (or filter by seller_id)
@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    """Get all cars, optionally filtered by seller_id"""
    try:
        seller_id = request.args.get('seller_id')
        
        from models.car import Car
        
        if seller_id:
            # Filter by seller_id
            from models import Seller
            seller = Seller.objects(id=seller_id).first()
            if not seller:
                return jsonify({'success': False, 'message': 'Seller not found'}), 404
            
            cars = Car.objects(seller=seller)
        else:
            # Get all cars
            cars = Car.objects()
        
        cars_list = []
        for car in cars:
            cars_list.append({
                'id': str(car.id),
                '_id': str(car.id),
                'brand': car.brand,
                'model': car.model,
                'color': getattr(car, 'color', ''),
                'year': car.year,
                'price': float(car.price),
                'fuel_type': car.fuel_type,
                'transmission': car.transmission,
                'car_type': car.car_type,
                'engine_size': getattr(car, 'engine_size', ''),
                'description': car.description,
                'images': car.images or [],
                'license_plate': car.license_plate,
                'vehicle_type': getattr(car, 'vehicle_type', 'Car'),
                'mileage': getattr(car, 'mileage', 0),
                'gas_system': getattr(car, 'gas_system', ''),
                'sold': getattr(car, 'sold', False),
                'sold_out': getattr(car, 'sold_out', False),
                'views': getattr(car, 'views', 0),
                'created_at': car.created_at.isoformat() if hasattr(car, 'created_at') else None,
                'seller': {
                    'id': str(car.seller.id),
                    'username': car.seller.username,
                    'business_name': car.seller.business_name,
                    'email': car.seller.email,
                    'phonenumber': car.seller.phonenumber,
                    'contact_info': car.seller.contact_info
                } if car.seller else None
            })
        
        return jsonify({
            'success': True,
            'cars': cars_list,
            'total': len(cars_list)
        }), 200
    
    except Exception as e:
        print(f"Get cars error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET SINGLE CAR BY ID
@cars_bp.route('/cars/<car_id>', methods=['GET'])
def get_car_by_id(car_id):
    """Get single car by ID"""
    try:
        from models.car import Car
        car = Car.objects(id=car_id).first()
        
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        car_data = {
            'id': str(car.id),
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'price': float(car.price),
            'fuel_type': car.fuel_type,
            'transmission': car.transmission,
            'car_type': car.car_type,
            'description': car.description,
            'images': car.images or [],
            'license_plate': car.license_plate,
            'sold': getattr(car, 'sold', False),
            'sold_out': getattr(car, 'sold_out', False),
            'views': getattr(car, 'views', 0),
            'created_at': car.created_at.isoformat() if hasattr(car, 'created_at') else None,
            'seller': {
                'id': str(car.seller.id),
                'username': car.seller.username,
                'business_name': car.seller.business_name,
                'email': car.seller.email,
                'phonenumber': car.seller.phonenumber,
                'contact_info': car.seller.contact_info
            } if car.seller else None
        }
        
        return jsonify({
            'success': True,
            'car': car_data
        }), 200
    
    except Exception as e:
        print(f"Get car error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  UPDATE CAR STATUS (Mark as sold out)
@cars_bp.route('/cars/<car_id>/sold', methods=['PATCH'])
@jwt_required()
def mark_car_sold(car_id):
    """Mark a car as sold or unsold"""
    try:
        from models.car import Car
        
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        data = request.get_json() or {}
        
        # Update sold_out field from request
        if 'sold_out' in data:
            car.sold_out = data.get('sold_out')
        elif 'sold' in data:
            car.sold_out = data.get('sold')
        else:
            car.sold_out = True
            
        car.save()
        
        print(f"Car {car_id} updated: sold_out = {car.sold_out}")
        
        return jsonify({
            'success': True,
            'message': 'Car status updated',
            'sold_out': car.sold_out
        }), 200
    
    except Exception as e:
        print(f"Update car status error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  DELETE CAR
@cars_bp.route('/cars/<car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    """Delete a car listing"""
    try:
        from models.car import Car
        
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        car.delete()
        
        return jsonify({
            'success': True,
            'message': 'Car deleted successfully'
        }), 200
    
    except Exception as e:
        print(f"Delete car error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET ADMIN ALL CARS
@cars_bp.route('/admin/cars', methods=['GET'])
@jwt_required()
def admin_get_cars():
    """Get all cars for admin"""
    try:
        from models.car import Car
        
        cars = Car.objects()
        cars_list = []
        for car in cars:
            cars_list.append({
                '_id': str(car.id),
                'id': str(car.id),
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': float(car.price),
                'license_plate': car.license_plate,
                'seller': {
                    'username': car.seller.username if car.seller else 'Unknown'
                },
                'sold_out': getattr(car, 'sold_out', False),
                'created_at': car.created_at.isoformat() if hasattr(car, 'created_at') else None
            })
        
        return jsonify({
            'success': True,
            'cars': cars_list
        }), 200
    
    except Exception as e:
        print(f"Admin get cars error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  UPDATE CAR (Admin & Seller)
@cars_bp.route('/cars/<car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    """Update car details"""
    try:
        from models.car import Car
        
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({'success': False, 'error': 'Car not found'}), 404
        
        data = request.get_json() or {}
        
        # ✅ Update all car fields
        if 'brand' in data:
            car.brand = data['brand']
        if 'model' in data:
            car.model = data['model']
        if 'year' in data:
            car.year = data['year']
        if 'price' in data:
            car.price = float(data['price'])
        if 'fuel_type' in data:
            car.fuel_type = data['fuel_type']
        if 'transmission' in data:
            car.transmission = data['transmission']
        if 'engine_size' in data:
            car.engine_size = data['engine_size']
        if 'mileage' in data:
            car.mileage = int(data['mileage']) if data.get('mileage') else 0
        if 'color' in data:
            car.color = data['color']
        if 'car_type' in data:
            car.car_type = data['car_type']
        if 'drive_system' in data:
            car.drive_system = data['drive_system']
        if 'gas_system' in data:
            car.gas_system = data['gas_system']
        if 'description' in data:
            car.description = data['description']
        if 'license_plate' in data:
            car.license_plate = data['license_plate']
        if 'sold_out' in data:
            car.sold_out = data['sold_out']
        if 'sold' in data:
            car.sold = data['sold']
        
        car.save()
        
        print(f'[CAR UPDATE] Car {car_id} updated successfully')
        
        return jsonify({
            'success': True,
            'message': 'Car updated successfully'
        }), 200
        
    except Exception as e:
        print(f'Update car error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


#  UPDATE CAR (Admin)
@cars_bp.route('/admin/cars/<car_id>', methods=['PUT'])
@jwt_required()
def admin_update_car(car_id):
    """Update car details (admin)"""
    try:
        from models.car import Car
        
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        data = request.get_json() or {}
        
        if data.get('brand'):
            car.brand = data.get('brand')
        if data.get('model'):
            car.model = data.get('model')
        if data.get('year'):
            car.year = data.get('year')
        if data.get('price'):
            car.price = float(data.get('price'))
        if data.get('description'):
            car.description = data.get('description')
        if data.get('license_plate'):
            car.license_plate = data.get('license_plate')
        if 'sold_out' in data:
            car.sold_out = data.get('sold_out')
        
        car.save()
        
        return jsonify({
            'success': True,
            'message': 'Car updated successfully'
        }), 200
    
    except Exception as e:
        print(f"Update car error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  DELETE CAR (Admin)
@cars_bp.route('/admin/cars/<car_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_car(car_id):
    """Delete a car (admin)"""
    try:
        from models.car import Car
        
        car = Car.objects(id=car_id).first()
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        car.delete()
        
        return jsonify({
            'success': True,
            'message': 'Car deleted successfully'
        }), 200
    
    except Exception as e:
        print(f"Delete car error: {str(e)}")
        return jsonify({'error': str(e)}), 500