

import pandas as pd 
import os
#from pytube import YouTube
from moviepy.editor import VideoFileClip
# Importar o módulo unicodedata para converter caracteres unicode
import unicodedata
# Importar o módulo re para usar expressões regulares
import re
from modules import help_functions as hp

from pytubefix import YouTube
from pytubefix.cli import on_progress
 
#url = "url"
 
#yt = YouTube(url, on_progress_callback = on_progress)
#print(yt.title)
 
#ys = yt.streams.get_highest_resolution()
#ys.download()

def download_video(video_url, dir):
    
    try:
            
        yt = YouTube(video_url, on_progress_callback = on_progress)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        
        video_stream.download(output_path=dir)

    except Exception as erro:
        print(erro)
        print('Error Downloading video! aqui')

def convert_mp4_to_mp3(dir_mp4,audio_filename, dir_mp3):
    
    try:
        video_clip = VideoFileClip(dir_mp4)
        audio_clip = video_clip.audio
        #audio_filename = os.path.join(dir_mp3, audio_filename)
        audio_filename = f"{dir_mp3}/{audio_filename}"
        audio_clip.write_audiofile(audio_filename)
        # Limpar arquivos temporários
        video_clip.close()
        audio_clip.close()
        
        print(f'O vídeo foi baixado e convertido em MP3: {audio_filename}')
        
    except Exception as erro:
        print(erro)
        print('Error converting the video!')


def download_mp3(video_url, output_dir,temp_dir):

    try: 
        download_video(video_url, temp_dir)

        arquivo_temp = hp.listar_arquivos_em_pasta(temp_dir)

        video_filename = f'{temp_dir}/{arquivo_temp[0]}'

        audio_filename = f"{hp.renomear_string(arquivo_temp[0].split('.')[0])}.mp3"

        print(arquivo_temp[0].split('/')[-1])
        print(temp_dir)
        #hp.renomear_arquivo(f'{temp_dir}', arquivo_temp[0].split('/')[-1])
        caminho = temp_dir
        nome = arquivo_temp[0].split('/')[-1]
        # Obter a extensão do arquivo
        print(nome)
        nome_raw = nome.split('.')[0]
        print(nome_raw)
        extensao = nome.split('.')[1]
        # Normalizar o nome novo para a forma NFKD, que separa os caracteres base dos diacríticos
        nome = unicodedata.normalize('NFKD', nome_raw)
        # Remover os diacríticos usando uma compreensão de lista
        nome = ''.join([c for c in nome if not unicodedata.combining(c)])
        # Substituir os espaços por underline usando o método replace
        nome = nome.replace(' ', '_')
        # Remover os caracteres especiais usando uma expressão regular
        nome = re.sub('[^A-Za-z0-9_]', '', nome)
        # Juntar o nome novo com a extensão do arquivo
        nome_novo = nome + '.' + extensao
        # Obter o caminho novo do arquivo
        caminho_novo = f"{caminho}/{nome_novo}"

        # Renomear o arquivo usando o método rename
        os.rename(video_filename, f'{os.getcwd()}/{caminho_novo}')

        print(caminho_novo)
        # Converter o vídeo em 
        audio_filename = convert_mp4_to_mp3(caminho_novo,audio_filename, output_dir)

        os.remove(caminho_novo)

    except Exception as erro:
        print(erro)
        print('Error converting the video!')

def download_playlist_mp3(playlist_name,path_playlist,output_dir,temp_dir):
    try:

        playlist = pd.read_csv(path_playlist).dropna().reset_index(drop=True) 
        # Full path of the new folder
        full_path = os.path.join(os.getcwd(),output_dir, playlist_name)

        # Create the new folder
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            print(f"Folder '{playlist_name}' created at '{full_path}'")
        else:
            print(f"Folder '{playlist_name}' already exists at '{full_path}'")

        # URL do vídeo do YouTube
        output_dir_playlist = os.path.join(output_dir, playlist_name)

        for i in range(len(playlist)):
            video_url = f"https://www.youtube.com{playlist['link'][i]}"
            download_mp3(video_url, output_dir_playlist,temp_dir)
    
    except Exception as erro:
        print(erro)
        print('Error downloading the playlist!')

