// Create file: e:\ProjectFainal\backend\routes\messages.js
const express = require('express')
const router = express.Router()
const Message = require('../models/Message')
const Conversation = require('../models/Conversation')

// Get all conversations for a user
router.get('/conversations/:username', async (req, res) => {
  try {
    const username = req.params.username
    const conversations = await Conversation.find({
      $or: [
        { userOne: username },
        { userTwo: username }
      ]
    }).sort({ updatedAt: -1 })

    res.json({
      success: true,
      conversations: conversations.map(conv => ({
        _id: conv._id,
        otherUser: conv.userOne === username ? conv.userTwo : conv.userOne,
        otherUserId: conv.userOne === username ? conv.userTwoId : conv.userOneId,
        lastMessage: conv.lastMessage,
        lastMessageTime: conv.lastMessageAt,
        unreadCount: conv.userOne === username ? conv.unreadCountOne : conv.unreadCountTwo,
        accountType: conv.userOne === username ? conv.userTwoType : conv.userOneType
      }))
    })
  } catch (error) {
    console.error('Error fetching conversations:', error)
    res.status(500).json({
      success: false,
      message: 'Error fetching conversations'
    })
  }
})

// Get messages for a conversation
router.get('/messages/:conversationId', async (req, res) => {
  try {
    const conversationId = req.params.conversationId
    const messages = await Message.find({
      conversationId: conversationId
    }).sort({ createdAt: 1 })

    res.json({
      success: true,
      messages: messages
    })
  } catch (error) {
    console.error('Error fetching messages:', error)
    res.status(500).json({
      success: false,
      message: 'Error fetching messages'
    })
  }
})

// Send a message
router.post('/messages', async (req, res) => {
  try {
    const { sender, senderId, recipientUsername, recipientId, text, conversationId } = req.body

    if (!sender || !recipientUsername || !text) {
      return res.status(400).json({
        success: false,
        message: 'Missing required fields'
      })
    }

    // Create message
    const message = new Message({
      conversationId: conversationId,
      sender: sender,
      senderId: senderId,
      recipient: recipientUsername,
      recipientId: recipientId,
      text: text,
      timestamp: new Date()
    })

    await message.save()

    // Update conversation
    await Conversation.findByIdAndUpdate(
      conversationId,
      {
        lastMessage: text,
        lastMessageAt: new Date(),
        $inc: {
          unreadCountTwo: sender === recipientUsername ? 0 : 1
        }
      },
      { new: true }
    )

    res.json({
      success: true,
      messageId: message._id,
      message: 'Message sent successfully'
    })
  } catch (error) {
    console.error('Error sending message:', error)
    res.status(500).json({
      success: false,
      message: 'Error sending message'
    })
  }
})

// Create conversation
router.post('/conversations/create', async (req, res) => {
  try {
    const { username, otherUsername, accountType } = req.body

    if (!username || !otherUsername) {
      return res.status(400).json({
        success: false,
        message: 'Missing required fields'
      })
    }

    // Check if conversation already exists
    let conversation = await Conversation.findOne({
      $or: [
        { userOne: username, userTwo: otherUsername },
        { userOne: otherUsername, userTwo: username }
      ]
    })

    if (conversation) {
      return res.json({
        success: true,
        conversationId: conversation._id,
        message: 'Conversation already exists'
      })
    }

    // Get user IDs from database if needed
    // For now, using usernames as IDs
    conversation = new Conversation({
      userOne: username,
      userOneId: username,
      userOneType: 'buyer',
      userTwo: otherUsername,
      userTwoId: otherUsername,
      userTwoType: accountType || 'seller',
      lastMessage: '',
      lastMessageAt: new Date(),
      unreadCountOne: 0,
      unreadCountTwo: 0
    })

    await conversation.save()

    res.json({
      success: true,
      conversationId: conversation._id,
      message: 'Conversation created successfully'
    })
  } catch (error) {
    console.error('Error creating conversation:', error)
    res.status(500).json({
      success: false,
      message: 'Error creating conversation'
    })
  }
})

// Mark conversation as read
router.put('/conversations/:conversationId/read', async (req, res) => {
  try {
    const conversationId = req.params.conversationId

    const conversation = await Conversation.findByIdAndUpdate(
      conversationId,
      {
        unreadCountOne: 0,
        unreadCountTwo: 0
      },
      { new: true }
    )

    res.json({
      success: true,
      message: 'Conversation marked as read'
    })
  } catch (error) {
    console.error('Error marking conversation as read:', error)
    res.status(500).json({
      success: false,
      message: 'Error marking conversation as read'
    })
  }
})

module.exports = router