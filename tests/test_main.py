import os
import csv
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import gerar_pdf, tarefa_pdf, main

def test_gerar_pdf_single(temp_test_dir, mock_csv_data):
    """Testa a geração de um único arquivo PDF"""
    output_file = 'test_report.pdf'
    output_path = temp_test_dir['output_dir'] / output_file
    
    # Gera PDF com dados de exemplo
    gerar_pdf(mock_csv_data[1:], output_file)
    
    # Verify PDF was created
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_tarefa_pdf_thread(temp_test_dir, mock_csv_data):
    """Testa a geração de PDF em uma thread"""
    # Executa a geração do PDF em uma thread
    tarefa_pdf(mock_csv_data[1:], 0)
    
    # Verifica se o PDF foi criado
    output_path = temp_test_dir['output_dir'] / 'relatorio_1.pdf'
    assert output_path.exists()
    assert output_path.stat().st_size > 0

def test_main_function_complete_workflow(temp_test_dir, mock_csv_data):
    """Testa o fluxo completo com múltiplas threads"""
    # Create test CSV file
    csv_path = temp_test_dir['data_dir'] / 'dados.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in mock_csv_data:
            writer.writerow(row)
    
    # Run main function
    main()
    
    # Verify PDF files were created
    expected_files = [f'relatorio_{i}.pdf' for i in range(1, 2)]  # Only 1 report with our test data
    for filename in expected_files:
        pdf_path = temp_test_dir['output_dir'] / filename
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0

def test_main_with_empty_csv(temp_test_dir):
    """Testa o tratamento de arquivo CSV vazio"""
    # Cria arquivo CSV vazio
    csv_path = temp_test_dir['data_dir'] / 'dados.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Nome', 'Valor'])  # Only header
    
    # Run main function - should not create any PDFs
    main()
    
    # Verify no PDF files were created
    pdf_files = list(temp_test_dir['output_dir'].glob('*.pdf'))
    assert len(pdf_files) == 0

def test_main_missing_csv(temp_test_dir):
    """Testa o tratamento de arquivo CSV ausente"""
    with pytest.raises(FileNotFoundError):
        main()

def test_main_invalid_csv_format(temp_test_dir):
    """Testa o tratamento de formato CSV inválido"""
    # Cria CSV com formato inválido
    csv_path = temp_test_dir['data_dir'] / 'dados.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        f.write('Invalid,CSV,Format\nNo,proper,columns')
    
    with pytest.raises(IndexError):  # Should raise when trying to access data columns
        main()