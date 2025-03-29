import os
from os import listdir
from os.path import isfile, join
from pypdf import PdfWriter
from tqdm import tqdm
import fitz
from pathlib import Path

class ProcessToRag:
    def __init__(
            self, 
            input_folder: str, 
            output_folder: str=None, 
            file_name: str='RAG_output', 
            process_type: str='megre', 
            translation: bool =False, 
            merge_file_count: int = 10, 
            encoding: str="utf-8"
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

    def process(self):
        self._get_files()
        if self.process_type == 'megre':
            self._merge_files()
            if self.logs:
                self._save_logs()
        elif self.process_type == 'mid':
            '''
            → ekstrakcja + czyszczenie
            → chunking (z limitem tokenów)
            → tłumaczenie na EN (tylko jeśli embedding jest EN-only)
            '''
            self._extract_content()
        else:
            print(f'Error! Wrong process type. Available options: [\'lite\', \'full\']. Selected: {self.process_type}')

    def _get_files(self):
        try:
            self.files_list = [f for f in listdir(self.input_folder) if isfile(join(self.input_folder, f)) and f.endswith('.pdf')]
            self.total_files = len(self.files_list)
        except Exception as e:
            self.logs.append(f'Error in getting files: {e}')

    def _extract_content(self):
        for file in self.files_list:
            file_name = file.split(".")[0]
            file_path = join(self.output_folder, f'{file}')
            doc = fitz.open(file_path)
            output_path = Path(self.output_folder)
            output_path = output_path/f"texts/"
            output_path.mkdir(exist_ok=True, parents=True)

            for page_num in tqdm(range(len(doc)), desc="Content extracting: "):
                page = doc[page_num]
                blocks = page.get_text("blocks")
                paragrapsh = self._get_paragraphs(blocks) 
                i = 1   
                for paragraph in paragrapsh:
                    final_content = self._clean_content(paragraph)
                    if not final_content:
                        continue
                    # if (self.translation): pass # placeholder
                    full_output_path = output_path/f"{file_name}_{page_num + 1}_{i}.txt"
                    if not os.path.exists(full_output_path):
                        with open(full_output_path, 'w', encoding=self.encoding) as f:
                            f.write(final_content)
                    i += 1

    def _get_paragraphs(self, blocks, y_gap_threshold=5):
        blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  
        paragraphs = []
        current_para = []
        last_y = None

        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            text = text.strip()
            if not text:
                continue

            if last_y is not None and abs(y0 - last_y) > y_gap_threshold:
                # przerwa między blokami = nowy akapit
                paragraphs.append(" ".join(current_para))
                current_para = []

            current_para.append(text)
            last_y = y1

        if current_para:
            paragraphs.append(" ".join(current_para))

        return paragraphs

    def _clean_content(self, text):
        lines = text.splitlines()
        cleaned = []
        for line in lines:
            if line.strip().isdigit():
                continue
            if line.strip() in ("", " ", "\n"):
                continue
            line = line.replace("-\n", "")
            # line = line.replace("\n", " ")
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
            self.logs.append(f'Error in merging files: {e}')

    def _get_merge_chunks_size(self):
        return [self.files_list[i:i + self.merge_file_count] for i in range(0, self.total_files, self.merge_file_count)]

    def _save_logs(self):
        log_path = join(self.output_folder, 'process_to_rag_logs.txt')
        with open(log_path, 'w') as f:
            for log in self.logs:
                f.write(log + '\n')

if __name__ == '__main__':
    # input_folder = input('Enter the input folder path: ')
    input_folder = r"C:\Users\micha\OneDrive\Pulpit\test"
    process = ProcessToRag(input_folder=input_folder, process_type="mid")
    process.process()
