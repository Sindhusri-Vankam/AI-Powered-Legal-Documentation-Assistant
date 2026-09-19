const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
const Document = require("../models/Document");

const createDocument = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "Please upload a PDF or DOCX file",
      });
    }

    const formData = new FormData();

    formData.append(
      "file",
      fs.createReadStream(req.file.path)
    );

    const aiResponse = await axios.post(
      "http://127.0.0.1:8000/api/process",
      formData,
      {
        headers: {
          ...formData.getHeaders(),
        },
      }
    );

    const document = await Document.create({
      user: req.user.userId,
      fileName: req.file.originalname,
      filePath: req.file.path,
      fileType: req.file.mimetype,
      extractedText: aiResponse.data.extractedText || "",
      summary: aiResponse.data.summary || "",
    });

    res.status(201).json({
      success: true,
      message: "Document uploaded and processed successfully",
      document,
      aiAnalysis: {
        clauses: aiResponse.data.clauses || {},
        risks: aiResponse.data.risks || [],
      },
    });
  } catch (error) {
    console.error(
      "AI processing failed:",
      error.response?.data || error.message
    );

    res.status(500).json({
      success: false,
      message: "Document uploaded but AI processing failed",
      error: error.message,
    });
  }
};

const getDocuments = async (req, res) => {
  try {
    const documents = await Document.find({
      user: req.user.userId,
    }).sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      documents,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Server error",
      error: error.message,
    });
  }
};

module.exports = {
  createDocument,
  getDocuments,
};