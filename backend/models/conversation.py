# filepath: e:\ProjectFainal\backend\models\conversation.py
from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, IntField, EmbeddedDocumentListField

class Conversation(Document):
    user_one = StringField(required=True)
    user_one_id = StringField()
    user_one_type = StringField(default='buyer')
    user_two = StringField(required=True)
    user_two_id = StringField()
    user_two_type = StringField(default='seller')
    last_message = StringField()
    last_message_at = DateTimeField(default=datetime.utcnow)
    unread_count_one = IntField(default=0)
    unread_count_two = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'conversations',
        'indexes': [
            'user_one',
            'user_two',
            ('user_one', 'user_two')
        ]
    }
    
    def to_dict(self, username=None):
        if username == self.user_one:
            other_user = self.user_two
            other_user_id = self.user_two_id
            other_user_type = self.user_two_type
            unread = self.unread_count_one
        else:
            other_user = self.user_one
            other_user_id = self.user_one_id
            other_user_type = self.user_one_type
            unread = self.unread_count_two
        
        return {
            '_id': str(self.id),
            'otherUser': other_user,
            'otherUserId': other_user_id,
            'accountType': other_user_type,
            'lastMessage': self.last_message or 'No messages yet',
            'lastMessageTime': self.last_message_at.isoformat() if self.last_message_at else None,
            'unreadCount': unread
        }