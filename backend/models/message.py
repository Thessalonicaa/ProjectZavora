# filepath: e:\ProjectFainal\backend\models\message.py
from datetime import datetime
from mongoengine import Document, StringField, ReferenceField, DateTimeField, BooleanField

class Message(Document):
    conversation_id = StringField(required=True)
    sender = StringField(required=True)
    sender_id = StringField()
    recipient = StringField(required=True)
    recipient_id = StringField()
    text = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    is_read = BooleanField(default=False)
    
    meta = {
        'collection': 'messages',
        'indexes': ['conversation_id', 'sender', 'recipient']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            '_id': str(self.id),
            'conversationId': self.conversation_id,
            'sender': self.sender,
            'senderId': self.sender_id,
            'recipient': self.recipient,
            'recipientId': self.recipient_id,
            'text': self.text,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'isRead': self.is_read
        }