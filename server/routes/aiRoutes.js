const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const { askQuestion } = require("../controllers/aiController");

const router = express.Router();

router.post("/qa", protect, askQuestion);

module.exports = router;
