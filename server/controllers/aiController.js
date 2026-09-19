const Document = require("../models/Document");
const axios = require("axios");

const askQuestion = async (req, res) => {
  try {
    const { documentId, question } = req.body;

    if (!documentId || !question) {
      return res.status(400).json({
        success: false,
        message: "documentId and question are required",
      });
    }

    const document = await Document.findOne({
      _id: documentId,
      user: req.user.userId,
    });

    if (!document) {
      return res.status(404).json({
        success: false,
        message: "Document not found",
      });
    }

    const aiResponse = await axios.post(
      "http://127.0.0.1:8000/api/qa",
      {
        document_text: document.extractedText,
        question: question,
      }
    );

    res.status(200).json({
      success: true,
      question: question,
      answer: aiResponse.data.answer,
      relevant_chunks: aiResponse.data.relevant_chunks || [],
    });
  } catch (error) {
    console.error(
      "Q&A processing failed:",
      error.response?.data || error.message
    );

    res.status(500).json({
      success: false,
      message: "Failed to process question",
      error: error.message,
    });
  }
};

module.exports = {
  askQuestion,
};
