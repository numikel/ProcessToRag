# 🧠 ProcessToRag

**ProcessToRag** is a modular Python tool for processing and preparing PDF documents for downstream tasks such as Retrieval-Augmented Generation (RAG), document classification, archiving or knowledge extraction.  
It supports PDF merging, content extraction, paragraph segmentation and optional translation to English using the [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M) model.

## 🚀 Features

- ✅ Automatically detects `.pdf` files in a given folder  
- ✅ Merge mode: groups PDFs into chunks of defined size  
- ✅ Mid-processing mode: extracts, cleans and splits text into paragraphs  
- ✅ Optional translation to English (multi-language → English) via NLLB  
- ✅ Logging of processing steps and errors  
- ✅ Ready for integration with RAG pipelines or ML workflows

## 🛠 Requirements

Install dependencies (Python ≥ 3.9 recommended):

```bash
pip install -r requirements.txt
```

Ensure PyTorch is installed correctly – if using GPU, follow the installation instructions for your environment:
➡️ https://pytorch.org/get-started/locally/

## ▶️ How to Use
Run the script manually:

```bash
python process_to_rag.py
```

You can configure:
1) input_folder: where your PDF files are located
2) process_type: "merge" or "mid"
3) translation: True to enable translation to English
4) merge_file_count: number of files per merged PDF
5) logging: saves logs to process_to_rag_logs.txt

You can modify these directly in __main__ or extend with CLI (argparse support planned).

## 📌 Examples
Merge 25 PDF files into chunks of 10:
```python
ProcessToRag(input_folder="path/to/pdfs", process_type="merge", merge_file_count=10)
```

Extract and translate content from PDFs:
```python
ProcessToRag(input_folder="path/to/pdfs", process_type="mid", translation=True)
```

## 📁 Project Structure
```pgsql
PROCESSSTORAG/
├── process_to_rag.py            # Main script (PDF handling, extraction, logging)
├── translation_tool/
│   └── translation_tool.py      # Translation wrapper for NLLB-200
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
├── LICENSE                      # MIT license
├── .gitignore                   # Git ignore rules
```

## 🗂 Output
Extracted paragraphs are saved as .txt files in texts/ inside the output_folder.
Logs are written to process_to_rag_logs.txt.

## 📌 To-do
1) Add CLI support via argparse
2) Add full token-based chunking and embedding preparation
3) Support .docx and other formats
4) Add unit tests and CI pipeline

## 👤 Author
Made with ❤️ by Michał Kamiński

## 🧾 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute it as you wish.