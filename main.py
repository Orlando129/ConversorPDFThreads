import csv
import os
from threading import Thread
from fpdf import FPDF

CSV_PATH = 'data/dados.csv'
OUTPUT_DIR = 'output'

def gerar_pdf(dados, nome_arquivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Dados", ln=True, align='C')
    pdf.ln(10)

    for linha in dados:
        texto = f"ID: {linha[0]} | Nome: {linha[1]} | Valor: {linha[2]}"
        pdf.cell(200, 10, txt=texto, ln=True)

    pdf.output(os.path.join(OUTPUT_DIR, nome_arquivo))

def tarefa_pdf(linhas, indice):
    nome_arquivo = f'relatorio_{indice + 1}.pdf'
    gerar_pdf(linhas, nome_arquivo)
    print(f"[✓] PDF {nome_arquivo} gerado com sucesso.")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # pula cabeçalho
        
        # Valida o formato do cabeçalho
        if header != ['ID', 'Nome', 'Valor']:
            raise IndexError("Arquivo CSV tem formato inválido. Colunas esperadas: ID, Nome, Valor")
            
        dados = list(reader)
        if not dados:  # If no data after header
            return
            
    partes = [dados[i:i + 10] for i in range(0, len(dados), 10)]
    threads = []

    for i, parte in enumerate(partes):
        t = Thread(target=tarefa_pdf, args=(parte, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nTodos os PDFs foram gerados.")

if __name__ == '__main__':
    main()
