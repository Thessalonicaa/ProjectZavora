const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const Seller = require('../models/Seller');

router.post('/register-seller', async (req, res) => {
  try {
    const { username, email, password, shopName } = req.body;

    // Check if seller already exists
    const existingSeller = await Seller.findOne({ 
      $or: [{ username }, { email }, { shopName }] 
    });

    if (existingSeller) {
      return res.status(400).json({ 
        message: 'Username, email or shop name already exists' 
      });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Create new seller
    const seller = new Seller({
      username,
      email,
      password: hashedPassword,
      shopName,
      role: 'seller'
    });

    await seller.save();

    res.status(201).json({
      success: true,
      message: 'Seller registered successfully'
    });

  } catch (error) {
    res.status(500).json({ 
      message: 'Error registering seller', 
      error: error.message 
    });
  }
});

module.exports = router;
