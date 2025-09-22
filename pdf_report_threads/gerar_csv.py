# gera_csv.py
import csv

with open('data/dados.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Nome', 'Valor'])
    for i in range(1, 101):
        writer.writerow([i, f'Item {i}', f'R${i * 10:.2f}'])
