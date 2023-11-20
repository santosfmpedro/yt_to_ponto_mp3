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

# Definir a função de renomear um arquivo
def renomear_arquivo(caminho, nome):
  # Obter o nome antigo do arquivo
  nome_antigo = os.path.basename(caminho)
  # Obter a extensão do arquivo
  print(nome)
  nome_raw = nome.split('.')[0]
  extensao = nome.split('.')[1]
  # Normalizar o nome novo para a forma NFKD, que separa os caracteres base dos diacríticos
  nome = unicodedata.normalize('NFKD', nome)
  # Remover os diacríticos usando uma compreensão de lista
  nome = ''.join([c for c in nome if not unicodedata.combining(c)])
  # Substituir os espaços por underline usando o método replace
  nome = nome.replace(' ', '_')
  # Remover os caracteres especiais usando uma expressão regular
  nome = re.sub('[^A-Za-z0-9_]', '', nome)
  # Juntar o nome novo com a extensão do arquivo
  nome_novo = nome_raw + '.' + extensao
  # Obter o caminho novo do arquivo
  caminho_novo = f"{caminho}/{nome_novo}"
  # Renomear o arquivo usando o método rename
  os.rename(caminho, caminho_novo)
  # Retornar o caminho novo do arquivo
  return caminho_novo
