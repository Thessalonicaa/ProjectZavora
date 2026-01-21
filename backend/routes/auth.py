from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Seller

#  AUTHENTICATION BLUEPRINT

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

#  LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username:
            return jsonify({'error': 'ชื่อผู้ใช้ไม่ถูกต้อง'}), 400
        
        user = User.objects(username=username).first()
        
        if not user:
            return jsonify({'error': 'ชื่อผู้ใช้ไม่ถูกต้อง'}), 401
        
        # Check if user is admin - skip password check for admin
        user_role = getattr(user, 'role', '')
        is_admin = user_role == 'admin'
        
        if is_admin:
            # Admin can login without password or with any password
            token = create_access_token(identity=str(user.id))
            return jsonify({
                'success': True,
                'token': token,
                'user_id': str(user.id),
                'username': user.username,
                'role': 'admin',
                'is_admin': True,
                'is_seller': False
            }), 200
        
        # For non-admin users, check password normally
        if not password:
            return jsonify({'error': 'รหัสผ่านไม่ถูกต้อง'}), 400
        
        # Verify password
        if not check_password_hash(user.password, password):
            return jsonify({'error': 'รหัสผ่านไม่ถูกต้อง'}), 401
        
        token = create_access_token(identity=str(user.id))
        is_seller = getattr(user, 'is_seller', False)
        return jsonify({
            'success': True,
            'token': token,
            'user_id': str(user.id),
            'username': user.username,
            'role': getattr(user, 'role', 'user'),
            'is_seller': is_seller,
            'is_admin': False
        }), 200
    except Exception as e:
        print('Login error:', str(e))
        return jsonify({'error': 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'}), 500


#  REGISTER USER (ทั่วไป)
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if User.objects(username=data['username']).first():
            return jsonify({"msg": "Username already exists"}), 400

        hashed_pw = generate_password_hash(data['password'])
        user = User(username=data['username'], password=hashed_pw, role='user')
        user.save()

        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#  CHECK USERNAME AVAILABILITY
@auth_bp.route('/check-username/<username>', methods=['GET'])
def check_username(username):
    try:
        # ตรวจสอบชื่อผู้ใช้ในฐานข้อมูล (case-insensitive)
        user = User.objects(username__iexact=username).first()
        
        if user:
            return jsonify({'exists': True}), 200
        
        return jsonify({'exists': False}), 200
    
    except Exception as e:
        print(f'Check username error: {str(e)}')
        return jsonify({'error': str(e)}), 500


#  CHECK SHOP NAME AVAILABILITY
@auth_bp.route('/check-shop-name/<shop_name>', methods=['GET'])
def check_shop_name(shop_name):
    try:
        # ตรวจสอบชื่อร้านในฐานข้อมูล (case-insensitive)
        seller = Seller.objects(business_name__iexact=shop_name).first()
        
        if seller:
            return jsonify({'exists': True}), 200
        
        return jsonify({'exists': False}), 200
    
    except Exception as e:
        print(f'Check shop name error: {str(e)}')
        return jsonify({'error': str(e)}), 500


#  REGISTER SELLER (ผู้ขาย)
@auth_bp.route('/register/seller', methods=['POST'])
@jwt_required()
def register_seller():
    try:
        data = request.get_json() or {}

        # Use identity from JWT to get the existing user
        identity = get_jwt_identity()
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "ผู้ใช้ไม่ถูกต้อง หรือ token หมดอายุ"}), 401

        # ตรวจสอบว่าผู้ใช้เป็น seller แล้วหรือยัง
        if Seller.objects(user=user).first():
            return jsonify({"message": "User is already registered as a seller"}), 400

        # ต้องการอย่างน้อย email, business_name, contact_info
        required_fields = ['email', 'business_name', 'contact_info']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"Missing field: {field}"}), 400

        # ตรวจสอบ email ซ้ำใน collection ของ Seller
        if Seller.objects(email=data['email']).first():
            return jsonify({"message": "Email already registered for a seller"}), 400

        # สร้าง Seller ที่อ้างถึง user ที่ล็อกอินอยู่
        seller = Seller(
            user=user,
            username=user.username,
            email=data['email'],
            # เก็บ password เดิมจาก user (hashed)
            password=user.password,
            business_name=data['business_name'],
            contact_info=data['contact_info'],
            phonenumber=data.get('phonenumber'),
            role='seller'
        )
        seller.save()

        # อัปเดต role ของ User ให้เป็น seller
        user.role = 'seller'
        user.save()

        return jsonify({"message": "Seller registered successfully"}), 201

    except Exception as e:
        print(f"Register seller error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  CHECK SELLER STATUS (สถานะผู้ขาย)
@auth_bp.route('/check-seller-status/<user_id>', methods=['GET'])
@jwt_required()
def check_seller_status(user_id):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({'error': 'ไม่พบผู้ใช้'}), 404

        seller = Seller.objects(user=user).first()
        return jsonify({
            'is_seller': bool(seller),
            'seller_data': {
                'id': str(seller.id),
                'business_name': seller.business_name
            } if seller else None
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#  POST CAR LISTING
@auth_bp.route('/cars', methods=['POST'])
@jwt_required()
def post_car():
    try:
        identity = get_jwt_identity()
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        seller = Seller.objects(user=user).first()
        if not seller:
            return jsonify({"message": "User is not a seller"}), 403

        data = request.get_json() or {}

        # Validate required fields
        required_fields = ['brand', 'model', 'year', 'price', 'fuel_type', 'transmission', 'car_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"Missing field: {field}"}), 400

        # Validate fuel type
        valid_fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'Electric']
        if data.get('fuel_type') not in valid_fuel_types:
            return jsonify({"message": f"Invalid fuel type. Must be one of: {', '.join(valid_fuel_types)}"}), 400

        # Validate transmission
        valid_transmissions = ['Automatic', 'Manual']
        if data.get('transmission') not in valid_transmissions:
            return jsonify({"message": f"Invalid transmission. Must be one of: {', '.join(valid_transmissions)}"}), 400

        # Validate car type
        valid_car_types = ['Sedan', 'SUV', 'Pickup', 'Van', 'Sports']
        if data.get('car_type') not in valid_car_types:
            return jsonify({"message": f"Invalid car type. Must be one of: {', '.join(valid_car_types)}"}), 400

        # Create car listing
        from models.car import Car
        car = Car(
            seller=seller,
            brand=data.get('brand'),
            model=data.get('model'),
            year=int(data.get('year')),
            license_plate=data.get('licensePlate', ''),
            description=data.get('description', ''),
            price=float(data.get('price', 0)),
            fuel_type=data.get('fuel_type'),
            transmission=data.get('transmission'),
            car_type=data.get('car_type'),
            images=data.get('images', []),
            video_url=data.get('video_url', '')
        )
        car.save()

        return jsonify({
            "success": True,
            "message": "Car posted successfully",
            "car_id": str(car.id)
        }), 201

    except Exception as e:
        print(f"Post car error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET SELLER INFO
@auth_bp.route('/seller-info/<username>', methods=['GET'])
def get_seller_info(username):
    try:
        seller = Seller.objects(username=username).first()
        if not seller:
            return jsonify({"message": "Seller not found"}), 404
        
        return jsonify({
            "success": True,
            "seller": {
                "id": str(seller.id),
                "username": seller.username,
                "email": seller.email,
                "business_name": seller.business_name,
                "contact_info": seller.contact_info,
                "phonenumber": seller.phonenumber
            }
        }), 200
    
    except Exception as e:
        print(f"Get seller info error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  UPDATE PROFILE IMAGE
@auth_bp.route('/update-profile-image', methods=['POST'])
@jwt_required()
def update_profile_image():
    try:
        identity = get_jwt_identity()
        user = User.objects(id=identity).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Get base64 image from request
        data = request.get_json() or {}
        image_data = data.get('profileImage')

        if not image_data:
            return jsonify({"message": "No image provided"}), 400

        # Save image data to user
        user.profile_image = image_data
        user.save()

        return jsonify({
            "success": True,
            "message": "Profile image updated successfully",
            "profileImageUrl": image_data
        }), 200

    except Exception as e:
        print(f"Update profile image error: {str(e)}")
        return jsonify({'error': str(e)}), 500


#  GET PROFILE (with image)
@auth_bp.route('/get-profile', methods=['GET'])
def get_profile():
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({'success': False, 'message': 'Username required'}), 400
        
        user = User.objects(username=username).first()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Return user profile data - only fields that exist
        profile_data = {
            'success': True,
            'username': user.username,
            'profileImageUrl': getattr(user, 'profile_image', '') or '',
        }
        
        # Add optional fields if they exist
        if hasattr(user, 'email'):
            profile_data['email'] = user.email
        if hasattr(user, 'created_at'):
            profile_data['createdAt'] = str(user.created_at)
        
        return jsonify(profile_data), 200
    except Exception as e:
        print('Get profile error:', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500
