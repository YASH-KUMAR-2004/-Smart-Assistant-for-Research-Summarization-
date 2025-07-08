# 📄 Smart Assistant for Research Summarization
An AI-powered assistant that can deeply understand user-uploaded documents (PDF or TXT) and engage in contextual question answering and reasoning. Built using Python and Gradio, developed and tested on Google Colab.

## 🚀 Features
📁 Document Upload: Accepts PDF or TXT files.

📄 Auto Summary: Generates a concise summary (≤ 150 words) immediately after upload.

❓ Ask Anything: Users can ask free-form questions based on the document content.

🧠 Challenge Me: System poses logic-based questions, evaluates your answers, and provides document-based feedback.

🔍 Justified Responses: Every answer is backed by direct references to the document.

🛠 Tech Stack
Backend: Python (Colab Notebook)

Frontend: Gradio UI

NLP: Transformers, LangChain (optional), PyPDF / Text Extraction libs

Platform: Google Colab (for development and testing)

## 🧱 Project Structure

├── app/
│   ├── summarizer.py       # Auto-summary logic
│   ├── qa_module.py        # Question-answering logic
│   ├── logic_questions.py  # Challenge mode (Q&A evaluation)
│   ├── utils.py            # File handling, text extraction
│   └── interface.py        # Gradio interface definitions
├── example_docs/
│   └── sample.pdf          # Sample document for testing
├── README.md               # This file
├── requirements.txt        # Dependencies
└── main.ipynb              # Google Colab notebook (complete implementation)

## 🧪 How It Works
1. Upload Document
User uploads a PDF or TXT document via the Gradio interface.

2. Automatic Summary
A 150-word summary of the uploaded content is generated.

3. Interaction Modes
🗨️ Ask Anything
Users can ask any question about the document. The assistant provides a contextual answer along with a citation from the document (e.g., "as stated in paragraph 2...").

## 🧩 Challenge Me
The system:

Generates 3 logic/comprehension questions based on the document.

Takes user answers as input.

Evaluates the accuracy with explanations grounded in the original text.

## 🧠 Architecture & Reasoning Flow
          ┌────────────┐
          │ Upload Doc │
          └────┬───────┘
               │
     ┌─────────▼─────────┐
     │ Text Extraction   │
     └─────────┬─────────┘
               │
   ┌───────────▼───────────┐
   │   Document Summary    │
   └───────────┬───────────┘
               │
      ┌────────▼────────┐
      │ Interaction Mode│
      └────────┬────────┘
        ┌──────┴─────┐
   ┌────▼────┐   ┌────▼────┐
   │Ask Me   │   │Challenge│
   │Anything │   │   Me    │
   └─────────┘   └─────────┘

## ⚙️ Setup Instructions

📦 Requirements
Make sure the following are installed (or install via Colab):
```bash
    pip install gradio transformers PyPDF2
```
## 🧪 Running on Colab


Open main.ipynb in Google Colab.

Run all cells to launch the Gradio UI.

Upload your document and interact with the assistant.

## 📄 License
This project is licensed under the MIT License – feel free to use, modify, and distribute as needed.
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

👤 Author
[Yash Kumar]
📧 Email: yashkumar9887208373@gmail.com

