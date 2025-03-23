# 🗂️ ProcessToRag

**ProcessToRag** is a simple Python script that merges PDF files into grouped chunks — perfect for preparing documents for Retrieval-Augmented Generation (RAG) models or archiving purposes.

## 🚀 Features

- ✅ Automatically detects `.pdf` files in a given folder  
- ✅ Merges PDFs into user-defined chunk sizes  
- ✅ Supports a fast `lite` processing mode  
- ✅ Saves a log file in case of errors  

## 🛠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ How to Use
Run the script:

```bash
python process_to_rag.py
```

### You’ll be prompted to:
1) Enter the path to the folder containing PDF files
2) Choose the chunk size (e.g. 10 will group up to 10 PDFs per merged file)

### 📌 Example:
If you have 25 PDF files and set chunk size to 10, the script will generate 3 merged output files.

## 📁 Project Structure
```bash
process_to_rag/
├── process_to_rag.py       # Main script
├── requirements.txt        # Dependency list
├── README.md               # This file :)
└── .gitignore              # Git ignore rules
```

## 📌 To-do
1) Add full processing mode
2) Add command-line arguments (argparse)
3) Support additional file formats

## 👤 Author
Made with ❤️ by Michał Kamiński

## 🧾 License
This project is licensed under the MIT License. You are free to use, modify, and distribute it as you wish.