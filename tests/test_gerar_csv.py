import os
import csv
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gerar_csv import gerar_csv_dados

def test_gerar_csv_success(temp_test_dir):
    """Testa a geração bem-sucedida do arquivo CSV"""
    csv_path = temp_test_dir['data_dir'] / 'dados.csv'
    
    # Gera o arquivo CSV
    gerar_csv_dados(str(csv_path))
    
    # Verifica se o arquivo existe
    assert csv_path.exists()
    
    # Verifica o conteúdo
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        
        # Verifica o cabeçalho
        assert data[0] == ['ID', 'Nome', 'Valor']
        
        # Verifica o número de linhas (100 itens + cabeçalho)
        assert len(data) == 101
        
        # Verifica o formato dos dados
        for i, row in enumerate(data[1:], 1):
            assert row[0] == str(i)
            assert row[1] == f'Item {i}'
            assert row[2] == f'R${i * 10:.2f}'

def test_gerar_csv_directory_not_exists(temp_test_dir):
    """Testa a geração do CSV quando o diretório não existe"""
    non_existent_dir = temp_test_dir['root'] / 'non_existent' / 'dados.csv'
    
    # Gera o CSV em um diretório inexistente
    gerar_csv_dados(str(non_existent_dir))
    
    # Verifica se o diretório foi criado e o arquivo existe
    assert non_existent_dir.exists()
    assert non_existent_dir.parent.is_dir()

def test_gerar_csv_permission_error(temp_test_dir, monkeypatch):
    """Testa a geração do CSV com permissões insuficientes"""
    csv_path = temp_test_dir['data_dir'] / 'dados.csv'
    
    def mock_open(*args, **kwargs):
        raise PermissionError("Permissão negada")
    
    monkeypatch.setattr('builtins.open', mock_open)
    
    with pytest.raises(PermissionError):
        gerar_csv_dados(str(csv_path))