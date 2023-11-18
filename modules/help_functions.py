import pandas as  pd 
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
# Importar o módulo unicodedata para converter caracteres unicode
import unicodedata
# Importar o módulo re para usar expressões regulares
import re

# Definir a função de renomear uma string
def renomear_string(string):
  # Normalizar a string para a forma NFKD, que separa os caracteres base dos diacríticos
  string = unicodedata.normalize('NFKD', string)
  # Remover os diacríticos usando uma compreensão de lista
  string = ''.join([c for c in string if not unicodedata.combining(c)])
  # Substituir os espaços por underline usando o método replace
  string = string.replace(' ', '_')
  # Remover os caracteres especiais usando uma expressão regular
  string = re.sub('[^A-Za-z0-9_]', '', string)
  # Retornar a string renomeada
  return string


def listar_arquivos_em_pasta(caminho_da_pasta):
    try:
        # Verifique se o caminho especificado é um diretório
        if os.path.isdir(caminho_da_pasta):
            # Use a função os.listdir() para listar os arquivos no diretório
            arquivos = os.listdir(caminho_da_pasta)
            return arquivos
        else:
            return "O caminho especificado não é um diretório válido."
    except Exception as e:
        return f"Ocorreu um erro ao listar os arquivos: {str(e)}"
