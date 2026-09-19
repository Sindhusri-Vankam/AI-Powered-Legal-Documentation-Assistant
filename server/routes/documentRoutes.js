const express = require("express");
const { protect } = require("../middleware/authMiddleware");
const upload = require("../middleware/uploadMiddleware");

const {
  createDocument,
  getDocuments,
} = require("../controllers/documentController");

const router = express.Router();

router.post("/", protect, createDocument);
router.get("/", protect, getDocuments);

router.post(
  "/upload",
  protect,
  upload.single("file"),
  createDocument
);

module.exports = router;