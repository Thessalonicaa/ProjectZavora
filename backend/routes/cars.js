const express = require('express');
const router = express.Router();
const multer = require('multer');
const Car = require('../models/Car');

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'public/uploads/cars')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname)
  }
});

const upload = multer({ storage: storage });

router.post('/', upload.array('images', 10), async (req, res) => {
  try {
    const imageUrls = req.files.map(file => `/uploads/cars/${file.filename}`);
    
    const car = new Car({
      brand: req.body.brand,
      model: req.body.model,
      year: req.body.year,
      licensePlate: req.body.licensePlate,
      description: req.body.description,
      price: req.body.price,
      images: imageUrls,
      seller: req.user._id // Assuming you have user authentication
    });

    await car.save();
    res.json({ success: true, car });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
