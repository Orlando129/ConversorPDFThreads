# gera_csv.py
import csv
import os

def gerar_csv_dados(filepath):
    """Gera arquivo CSV com dados de teste"""
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Nome', 'Valor'])
        for i in range(1, 101):
            writer.writerow([i, f'Item {i}', f'R${i * 10:.2f}'])

if __name__ == '__main__':
    gerar_csv_dados('data/dados.csv')
