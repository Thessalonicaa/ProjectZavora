// backend/routes/sellers.js
const express = require('express')
const router = express.Router()

// Get all sellers
router.get('/sellers', async (req, res) => {
  try {
    const User = require('../models/User')
    
    const sellers = await User.find({ is_seller: true }).select('username business_name email phonenumber contact_info')
    
    res.json({
      success: true,
      sellers: sellers.map(seller => ({
        username: seller.username,
        business_name: seller.business_name || seller.username,
        email: seller.email,
        phonenumber: seller.phonenumber,
        contact_info: seller.contact_info
      }))
    })
  } catch (error) {
    console.error('Error fetching sellers:', error)
    res.status(500).json({
      success: false,
      message: 'Error fetching sellers'
    })
  }
})

module.exports = router