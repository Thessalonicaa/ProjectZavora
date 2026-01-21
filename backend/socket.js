// Create file: e:\ProjectFainal\backend\socket.js
const socketIO = require('socket.io')
const Message = require('./models/Message')
const Conversation = require('./models/Conversation')

let io = null
const userSockets = {} // Map of username -> socket ID

const initializeSocket = (server) => {
  io = socketIO(server, {
    cors: {
      origin: 'http://localhost:3000',
      methods: ['GET', 'POST']
    }
  })

  io.on('connection', (socket) => {
    console.log('User connected:', socket.id)

    // User joins with their username
    socket.on('user_connect', (username) => {
      userSockets[username] = socket.id
      console.log(`${username} connected with socket ID: ${socket.id}`)
      socket.join(`user_${username}`)
      io.emit('user_online', { username, online: true })
    })

    // Send message
    socket.on('send_message', async (data) => {
      try {
        const { conversationId, sender, senderUsername, recipient, recipientUsername, text } = data

        // Save to database
        const message = new Message({
          conversationId,
          sender: senderUsername,
          senderId: sender,
          recipient: recipientUsername,
          recipientId: recipient,
          text,
          timestamp: new Date(),
          isRead: false
        })

        await message.save()

        // Update conversation
        await Conversation.findByIdAndUpdate(
          conversationId,
          {
            lastMessage: text,
            lastMessageAt: new Date()
          },
          { new: true }
        )

        // Send to both users
        const messageData = {
          _id: message._id,
          sender: senderUsername,
          text,
          timestamp: new Date().toISOString()
        }

        // Send to recipient
        if (userSockets[recipientUsername]) {
          io.to(`user_${recipientUsername}`).emit('receive_message', {
            conversationId,
            message: messageData
          })
        }

        // Send confirmation to sender
        socket.emit('message_sent', {
          conversationId,
          messageId: message._id,
          timestamp: message.timestamp
        })

        console.log(`Message from ${senderUsername} to ${recipientUsername}`)
      } catch (error) {
        console.error('Error sending message:', error)
        socket.emit('message_error', { error: 'Failed to send message' })
      }
    })

    // Mark conversation as read
    socket.on('mark_read', async (conversationId) => {
      try {
        await Conversation.findByIdAndUpdate(conversationId, {
          unreadCountOne: 0,
          unreadCountTwo: 0
        })
      } catch (error) {
        console.error('Error marking as read:', error)
      }
    })

    // User typing
    socket.on('typing', (data) => {
      const { recipientUsername, senderUsername } = data
      if (userSockets[recipientUsername]) {
        io.to(`user_${recipientUsername}`).emit('user_typing', {
          username: senderUsername
        })
      }
    })

    // User stop typing
    socket.on('stop_typing', (data) => {
      const { recipientUsername, senderUsername } = data
      if (userSockets[recipientUsername]) {
        io.to(`user_${recipientUsername}`).emit('user_stop_typing', {
          username: senderUsername
        })
      }
    })

    // Disconnect
    socket.on('disconnect', () => {
      for (let username in userSockets) {
        if (userSockets[username] === socket.id) {
          delete userSockets[username]
          io.emit('user_online', { username, online: false })
          console.log(`${username} disconnected`)
          break
        }
      }
    })
  })

  return io
}

const getIO = () => io

module.exports = {
  initializeSocket,
  getIO
}