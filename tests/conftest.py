import os
import pytest
import shutil

@pytest.fixture
def temp_test_dir(tmp_path):
    """Cria diretórios temporários para dados e saída dos testes"""
    data_dir = tmp_path / "data"
    output_dir = tmp_path / "output"
    data_dir.mkdir()
    output_dir.mkdir()
    
    # Configura o ambiente
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    yield {
        'root': tmp_path,
        'data_dir': data_dir,
        'output_dir': output_dir
    }
    
    # Cleanup
    os.chdir(original_cwd)
    shutil.rmtree(tmp_path)

@pytest.fixture
def mock_csv_data():
    """Retorna dados CSV de exemplo para testes"""
    return [
        ['ID', 'Nome', 'Valor'],
        ['1', 'Item 1', 'R$10.00'],
        ['2', 'Item 2', 'R$20.00'],
        ['3', 'Item 3', 'R$30.00']
    ]