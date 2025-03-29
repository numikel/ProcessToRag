from os import listdir
from os.path import isfile, join
from pypdf import PdfWriter
from tqdm import tqdm
from pathlib import Path
import fitz
import re
from langdetect import detect
from datetime import datetime

class ProcessToRag:
    def __init__(
            self, 
            input_folder: str, 
            output_folder: str=None, 
            file_name: str='RAG_output', 
            process_type: str='merge', 
            translation: bool =False, 
            merge_file_count: int = 10, 
            encoding: str="utf-8",
            logging: bool= True
            ):
        self.input_folder = input_folder
        self.output_folder = input_folder if output_folder is None else output_folder
        self.logs = []
        self.files_list = []
        self.total_files = 0
        self.file_name = file_name
        self.process_type = process_type
        self.translation = translation
        self.merge_file_count = merge_file_count
        self.encoding = encoding
        self.logging = logging

    def process(self):
        """Main function to run whole process"""
        self.logs.append(f'{self._get_current_timestamp()} | Process started')
        self._get_files()
        if self.process_type == 'merge':
            self._merge_files()
            self.logs.append(f'{self._get_current_timestamp()} | Merge process finished')
        elif self.process_type == 'mid':
            '''
            → ekstrakcja + czyszczenie
            → chunking (z limitem tokenów)
            → tłumaczenie na EN (tylko jeśli embedding jest EN-only)
            '''
            self._extract_content()
            self.logs.append(f'{self._get_current_timestamp()} | Mid level process finished')
        else:
            print(f'Error! Wrong process type. Available options: [\'lite\', \'full\']. Selected: {self.process_type}')
        if (self.logging): self._save_logs()

    def _get_files(self):
        """Method to get PDF files from selected folder"""
        try:
            self.files_list = [f for f in listdir(self.input_folder) if isfile(join(self.input_folder, f)) and f.endswith('.pdf')]
            self.total_files = len(self.files_list)
            self.logs.append(f'{self._get_current_timestamp()} | Get {self.total_files} files')
        except Exception as e:
            self.logs.append(f'{self._get_current_timestamp()} | Error in getting files: {e}')

    def _extract_content(self):
        self.logs.append(f'{self._get_current_timestamp()} | Extract content from files started')
        output_path = Path(self.output_folder) / "texts"
        output_path.mkdir(exist_ok=True, parents=True)

        for file in tqdm(self.files_list, desc="Documents processing", total=len(self.files_list)):
            file_name = Path(file).stem
            file_path = Path(self.output_folder) / file
            try:
                doc = fitz.open(file_path)
            except Exception as e:
                self.logs.append(f"Cannot open PDF {file_path}: {e}")
                continue
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                language = detect(text)
                paragraphs = self._get_paragraphs(text)
                for i, paragraph in enumerate(paragraphs, 1):
                    final_content = self._clean_content(paragraph)
                    if (self.translation and language != "en"): pass #placeholder for translation to english
                    full_output_path = output_path / f"{file_name}_{page_num + 1}_{i}.txt"
                    if not full_output_path.exists():
                        with open(full_output_path, 'w', encoding=self.encoding) as f:
                            f.write(final_content)
            self.logs.append(f'{self._get_current_timestamp()} | Content from file {file_name} extracted')

    def _get_paragraphs(self, text):
        return [p.strip() for p in re.split(r'(?:\r?\n\s*){2,}', text) if p.strip()]

    def _clean_content(self, text):
        lines = text.splitlines()
        cleaned = []
        for line in lines:
            if line.strip().isdigit():
                continue
            if line.strip() in ("", " ", "\n"):
                continue
            line = re.sub(r'-\s*\n', '', line)
            line = re.sub(r'\s*\n\s*', ' ', line)
            cleaned.append(line.strip())
        return " ".join(cleaned)

    def _merge_files(self):
        try:
            chunks = self._get_merge_chunks_size()
            for idx, chunk in tqdm(enumerate(chunks, start=1), desc='Merging files', unit='chunk'):
                merger = PdfWriter()
                for pdf in chunk:
                    merger.append(join(self.input_folder, pdf))
                output_filename = join(self.output_folder, f'{self.file_name}_{idx}.pdf')
                merger.write(output_filename)
                merger.close()
        except Exception as e:
            self.logs.append(f'{self._get_current_timestamp()} | Error in merging files: {e}')

    def _get_merge_chunks_size(self):
        return [self.files_list[i:i + self.merge_file_count] for i in range(0, self.total_files, self.merge_file_count)]

    def _get_current_timestamp(self):
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _save_logs(self):
        log_path = Path(self.output_folder, 'process_to_rag_logs.txt')
        with open(log_path, 'w') as f:
            for log in self.logs:
                f.write(log + '\n')

if __name__ == '__main__':
    # input_folder = input('Enter the input folder path: ')
    input_folder = r"C:\Users\micha\OneDrive\Pulpit\test"
    process = ProcessToRag(input_folder=input_folder, process_type="mid", translation=True)
    process.process()
