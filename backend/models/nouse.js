// Create file: e:\ProjectFainal\backend\models\Message.js
const mongoose = require('mongoose')

const messageSchema = new mongoose.Schema({
  conversationId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Conversation',
    required: true
  },
  sender: {
    type: String,
    required: true
  },
  senderId: {
    type: String
  },
  recipient: {
    type: String,
    required: true
  },
  recipientId: {
    type: String
  },
  text: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  isRead: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
})

module.exports = mongoose.model('Message', messageSchema)