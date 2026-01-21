
from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
import jwt
from flask import current_app as app

try:
    from db_init import db
except ImportError:
    from database import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders/purchases', methods=['GET'])
def get_purchases():
    """Get all purchases for a user"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Username required'}), 400
        
        # Get all cars marked as sold and where this user is associated as buyer
        purchases = list(db.orders.find({
            'buyer_username': username,
            'status': 'completed'
        }).sort('purchase_date', -1))
        
        # Convert ObjectIds to strings
        for purchase in purchases:
            purchase['_id'] = str(purchase['_id'])
            if 'car_id' in purchase:
                purchase['car_id'] = str(purchase['car_id'])
        
        return jsonify({
            'success': True,
            'orders': purchases
        }), 200
        
    except Exception as e:
        print(f"Error getting purchases: {str(e)}")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@orders_bp.route('/orders/sales', methods=['GET'])
def get_sales():
    """Get all sales for a seller"""
    try:
        username = request.args.get('username')
        
        if not username:
            return jsonify({'success': False, 'message': 'Username required'}), 400
        
        # Get all cars sold by this seller
        sales = list(db.orders.find({
            'seller_username': username,
            'status': 'completed'
        }).sort('sale_date', -1))
        
        # Convert ObjectIds to strings
        for sale in sales:
            sale['_id'] = str(sale['_id'])
            if 'car_id' in sale:
                sale['car_id'] = str(sale['car_id'])
        
        return jsonify({
            'success': True,
            'orders': sales
        }), 200
        
    except Exception as e:
        print(f"Error getting sales: {str(e)}")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500


@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order when car is sold"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'success': False, 'message': 'No token provided'}), 401
        
        # Verify token
        try:
            payload = jwt.decode(token, app.config.get('SECRET_KEY', 'secret'), algorithms=['HS256'])
            buyer_username = payload.get('username')
        except:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        data = request.get_json()
        car_id = data.get('car_id')
        seller_username = data.get('seller_username')
        
        if not car_id or not seller_username:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Get car details
        car = db.cars.find_one({'_id': ObjectId(car_id)})
        
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'}), 404
        
        # Create order record
        order = {
            'car_id': ObjectId(car_id),
            'buyer_username': buyer_username,
            'seller_username': seller_username,
            'car': {
                'brand': car.get('brand'),
                'model': car.get('model'),
                'year': car.get('year'),
                'price': car.get('price'),
                'images': car.get('images', []),
                'license_plate': car.get('license_plate')
            },
            'seller': {
                'username': seller_username,
                'business_name': car.get('business_name', '')
            },
            'buyer': {
                'username': buyer_username
            },
            'purchase_date': datetime.now(),
            'sale_date': datetime.now(),
            'status': 'completed',
            'amount': car.get('price')
        }
        
        result = db.orders.insert_one(order)
        
        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'Order created successfully',
                'order_id': str(result.inserted_id)
            }), 201
        else:
            return jsonify({'success': False, 'message': 'Failed to create order'}), 500
            
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500
