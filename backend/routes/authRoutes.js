const express = require('express');
const router = express.Router();
const bcrypt = require('bcrypt');
const User = require('../models/User');
const Seller = require('../models/Seller');

// Register regular user
router.post('/register', async (req, res) => {
  try {
    const { username, password, role } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const user = new User({
      username,
      password: hashedPassword,
      role: 'buyer'
    });
    
    await user.save();
    res.status(201).json({ message: 'User registered successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Register seller
router.post('/register-seller', async (req, res) => {
  try {
    const { username, email, password, shopName } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    
    const seller = new Seller({
      username,
      email,
      password: hashedPassword,
      shopName,
      role: 'seller'
    });
    
    await seller.save();
    res.status(201).json({ message: 'Seller registered successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Car search endpoint
router.get('/cars/search', async (req, res) => {
  try {
    const { q } = req.query;
    const cars = await Car.find({
      $or: [
        { name: { $regex: q, $options: 'i' } },
        { brand: { $regex: q, $options: 'i' } }
      ]
    }).limit(5);
    
    res.json(cars);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
