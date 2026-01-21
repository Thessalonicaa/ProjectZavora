# filepath: e:\ProjectFainal\backend\routes\messages.py
from flask import Blueprint, request, jsonify
from models.message import Message
from models.conversation import Conversation
from datetime import datetime
import uuid

messages_bp = Blueprint('messages', __name__, url_prefix='/api')

# Get all conversations for a user
@messages_bp.route('/conversations/<username>', methods=['GET'])
def get_conversations(username):
    try:
        conversations = Conversation.objects(
            __raw__={'$or': [{'user_one': username}, {'user_two': username}]}
        ).order_by('-updated_at')
        
        return jsonify({
            'success': True,
            'conversations': [conv.to_dict(username) for conv in conversations]
        }), 200
    except Exception as e:
        print(f'Error fetching conversations: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error fetching conversations'
        }), 500

# Get messages for a conversation
@messages_bp.route('/messages/<conversation_id>', methods=['GET'])
def get_messages(conversation_id):
    try:
        messages = Message.objects(conversation_id=conversation_id).order_by('timestamp')
        
        return jsonify({
            'success': True,
            'messages': [msg.to_dict() for msg in messages]
        }), 200
    except Exception as e:
        print(f'Error fetching messages: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error fetching messages'
        }), 500

# Send a message
@messages_bp.route('/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        
        sender = data.get('sender')
        sender_id = data.get('senderId')
        recipient = data.get('recipientUsername')
        recipient_id = data.get('recipientId')
        text = data.get('text')
        conversation_id = data.get('conversationId')
        
        if not sender or not recipient or not text:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Create message
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            sender_id=sender_id,
            recipient=recipient,
            recipient_id=recipient_id,
            text=text,
            timestamp=datetime.utcnow()
        )
        
        message.save()
        
        # Update conversation
        conversation = Conversation.objects(id=conversation_id).first()
        if conversation:
            conversation.last_message = text
            conversation.last_message_at = datetime.utcnow()
            conversation.updated_at = datetime.utcnow()
            conversation.save()
        
        return jsonify({
            'success': True,
            'messageId': str(message.id),
            'message': 'Message sent successfully'
        }, 200)
    except Exception as e:
        print(f'Error sending message: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error sending message'
        }), 500

# Create conversation
@messages_bp.route('/conversations/create', methods=['POST'])
def create_conversation():
    try:
        data = request.get_json()
        
        username = data.get('username')
        other_username = data.get('otherUsername')
        account_type = data.get('accountType', 'seller')
        
        if not username or not other_username:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Check if conversation already exists
        conversation = Conversation.objects(
            __raw__={
                '$or': [
                    {'user_one': username, 'user_two': other_username},
                    {'user_one': other_username, 'user_two': username}
                ]
            }
        ).first()
        
        if conversation:
            return jsonify({
                'success': True,
                'conversationId': str(conversation.id),
                'conversation': conversation.to_dict(username),
                'message': 'Conversation already exists'
            }), 200
        
        # Create new conversation
        conversation = Conversation(
            user_one=username,
            user_one_id=username,
            user_one_type='buyer',
            user_two=other_username,
            user_two_id=other_username,
            user_two_type=account_type,
            last_message='',
            last_message_at=datetime.utcnow()
        )
        
        conversation.save()
        
        return jsonify({
            'success': True,
            'conversationId': str(conversation.id),
            'conversation': conversation.to_dict(username),
            'message': 'Conversation created successfully'
        }), 201
    except Exception as e:
        print(f'Error creating conversation: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error creating conversation'
        }), 500

# Mark conversation as read
@messages_bp.route('/conversations/<conversation_id>/read', methods=['PUT'])
def mark_as_read(conversation_id):
    try:
        conversation = Conversation.objects(id=conversation_id).first()
        
        if not conversation:
            return jsonify({
                'success': False,
                'message': 'Conversation not found'
            }), 404
        
        conversation.unread_count_one = 0
        conversation.unread_count_two = 0
        conversation.updated_at = datetime.utcnow()
        
        conversation.save()
        
        return jsonify({
            'success': True,
            'message': 'Conversation marked as read'
        }), 200
    except Exception as e:
        print(f'Error marking conversation as read: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error marking conversation as read'
        }), 500

# Get all sellers
@messages_bp.route('/sellers', methods=['GET'])
def get_sellers():
    try:
        from models.car import Car
        
        # Get unique sellers from cars
        cars = Car.objects().distinct('seller_username')
        
        seller_list = []
        for seller_username in cars:
            if seller_username:
                seller_list.append({
                    'username': seller_username,
                    'business_name': f"{seller_username}'s Shop"
                })
        
        return jsonify({
            'success': True,
            'sellers': seller_list
        }), 200
    except Exception as e:
        print(f'Error fetching sellers: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error fetching sellers'
        }), 500

def get_seller_phone(username):
    """Get seller's phone number"""
    try:
        seller = Seller.objects(username=username).first()
        if not seller:
            return None
        return getattr(seller, 'phonenumber', '')
    except Exception as e:
        print(f"Error getting seller phone: {str(e)}")
        return None

# Delete conversation
@messages_bp.route('/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username or not conversation_id:
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Find conversation
        conversation = Conversation.objects(id=conversation_id).first()
        
        if not conversation:
            return jsonify({
                'success': False,
                'message': 'Conversation not found'
            }), 404
        
        # Verify user is part of conversation
        if conversation.user_one != username and conversation.user_two != username:
            return jsonify({
                'success': False,
                'message': 'Unauthorized to delete this conversation'
            }), 403
        
        # Delete all messages in this conversation
        Message.objects(conversation_id=conversation_id).delete()
        
        # Delete conversation
        conversation.delete()
        
        return jsonify({
            'success': True,
            'message': 'Conversation deleted successfully'
        }), 200
    except Exception as e:
        print(f'Error deleting conversation: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'Error deleting conversation'
        }), 500