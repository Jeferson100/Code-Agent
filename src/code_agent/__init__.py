import os
import sys

# Adiciona o diretório 'src' ao sys.path para permitir importações absolutas do projeto
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)
