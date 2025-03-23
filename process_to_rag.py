from os import listdir
from os.path import isfile, join
from pypdf import PdfWriter
from tqdm import tqdm

class ProcessToRag:
    def __init__(self, input_folder, output_folder=None, file_name='RAG_output', chunk_size=10, process_type='lite'):
        self.input_folder = input_folder
        self.output_folder = input_folder if output_folder is None else output_folder
        self.chunk_size = chunk_size
        self.logs = []
        self.files_list = []
        self.total_files = 0
        self.file_name = file_name
        self.process_type = process_type

    def process(self):
        if self.process_type == 'lite':
            self.get_files()
            self.merge_files()
            if self.logs:
                self.save_logs()
        elif self.process_type == 'full':
            pass  # Placeholder for extended functionality
        else:
            print(f'Error! Wrong process type. Available options: [\'lite\', \'full\']. Selected: {self.process_type}')

    def get_files(self):
        try:
            self.files_list = [f for f in listdir(self.input_folder) if isfile(join(self.input_folder, f)) and f.endswith('.pdf')]
            self.total_files = len(self.files_list)
        except Exception as e:
            self.logs.append(f'Error in getting files: {e}')

    def merge_files(self):
        try:
            chunks = self.get_chunks()
            for idx, chunk in tqdm(enumerate(chunks, start=1), desc='Merging files', unit='chunk'):
                merger = PdfWriter()
                for pdf in chunk:
                    merger.append(join(self.input_folder, pdf))
                output_filename = join(self.output_folder, f'{self.file_name}_{idx}.pdf')
                merger.write(output_filename)
                merger.close()
        except Exception as e:
            self.logs.append(f'Error in merging files: {e}')

    def get_chunks(self):
        return [self.files_list[i:i + self.chunk_size] for i in range(0, self.total_files, self.chunk_size)]

    def save_logs(self):
        log_path = join(self.output_folder, 'logs.txt')
        with open(log_path, 'w') as f:
            for log in self.logs:
                f.write(log + '\n')

if __name__ == '__main__':
    input_folder = input('Enter the input folder path: ')
    chunk_size = int(input('Enter the chunk size: '))
    process = ProcessToRag(input_folder=input_folder, chunk_size=chunk_size)
    process.process()
