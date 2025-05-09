import os
import shutil
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Função para extrair informações do PDF
def extract_data(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()

    print(text)
    cnpj_match = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', text)
    
    if cnpj_match:
        cnpj = cnpj_match.group().replace('.', '').replace('/', '').replace('-', '')
        
        razao_social_pattern = re.compile(re.escape(cnpj_match.group()) + r'\s*(.*?)\s*Período de Apuração', re.DOTALL)
        
        periodo_pattern = re.compile(r'Razão Social\s*\n\s*(\w+/\d{4})', re.DOTALL)
        
        print(periodo_pattern.pattern)

        razao_social_match = razao_social_pattern.search(text)
        periodo_match = periodo_pattern.search(text)

        if razao_social_match and periodo_match:
            razao_social = razao_social_match.group(1).strip()
            periodo_apuracao = periodo_match.group(1).replace('/', '-')
            return cnpj, razao_social, periodo_apuracao

    return None

# Função principal para processar arquivos PDF
def process_pdfs(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            data = extract_data(pdf_path)
            print(data)
            if data:
                cnpj, razao_social, periodo = data
                novo_nome = f"{cnpj} - {razao_social} - {periodo}.pdf"
                shutil.copy(pdf_path, os.path.join(output_directory, novo_nome))

    messagebox.showinfo("Processo concluído", "Todos os arquivos foram processados com sucesso.")

# Interface gráfica com tkinter
class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Utilitário de Renomeação PDF - DAS Simples Nacional")

        tk.Label(root, text="Diretório de entrada:").pack(pady=5)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)

        tk.Button(root, text="Selecionar Pasta", command=self.select_input_folder).pack(pady=5)

        tk.Label(root, text="Diretório de saída:").pack(pady=5)
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.pack(pady=5)

        tk.Button(root, text="Selecionar Pasta", command=self.select_output_folder).pack(pady=5)

        tk.Button(root, text="Processar PDF's", command=self.process_files).pack(pady=10)

    def select_input_folder(self):
        directory = filedialog.askdirectory()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, directory)

    def select_output_folder(self):
        directory = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, directory)

    def process_files(self):
        input_directory = self.input_entry.get()
        output_directory = self.output_entry.get()

        if not input_directory or not output_directory:
            messagebox.showerror("Erro", "Selecione ambos diretórios de entrada e saída.")
            return

        process_pdfs(input_directory, output_directory)

# Execução do aplicativo
if __name__ == '__main__':
    root = tk.Tk()
    app = PDFRenamerApp(root)
    root.mainloop()