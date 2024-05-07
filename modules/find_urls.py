import asyncio
from playwright.async_api import async_playwright
import sys
import pandas as pd 
import argparse
import time
import os 

local_file = os.path.abspath(__file__)

# Obter o diretório local do arquivo Python
local_path = os.path.dirname(local_file)

links_playlists_file = f'{os.path.join(local_path, "..")}/links_playlists.txt'
print(links_playlists_file)
path_save_links = f'github/yt_to_ponto_mp3/modules/output/links_musics'

async def scrape_youtube_playlist(playlist_url,playlist_name, path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = False)
        page = await browser.new_page()

        await page.goto(playlist_url)

        # Wait for the page to load completely (you may need to adjust the timeout)
         # Aguarde o carregamento completo da página (você pode precisar ajustar o timeout)
        #time.sleep(100)
        await page.wait_for_selector('#thumbnail')

        # Extraia títulos e links dos vídeos
        playlist_elements = await page.query_selector_all('#contents')
        print(playlist_elements)                                       
        video_elements = await page.query_selector_all('#thumbnail')
        
        playlist_data = []

        for video_element in video_elements:
           
            link = await video_element.get_attribute('href')
            print(link)
            playlist_data.append({ 'link': link}) #'title': title,

        await browser.close()

        # Create a DataFrame from the playlist_data
        df = pd.DataFrame(playlist_data)

        # Save the DataFrame to a CSV file
        df.to_csv(f'../{playlist_name}.csv', index=False, encoding='utf-8')

        return df

# loop = asyncio.get_event_loop()

# Extract the playlist name from the URL

# if __name__ == "__main__":
#     # Crie um argumento para o URL da playlist
#     parser = argparse.ArgumentParser(description='YouTube Playlist Scraper')
#     parser.add_argument('guide_playlist_path', type=str, help='guide_playlist Path ')
#     args = parser.parse_args()

#     guide_playlist_path = args.guide_playlist_path

playlists = pd.read_csv(links_playlists_file, header = None)

n_playlists = len(playlists[0]) 

for i in range(n_playlists):
    if playlists[1][i] == None:
        playlist_name = f'playlist_{[i]}'
    else:
        playlist_name = playlists[1][i]
        
    playlist_url = playlists[0][i]
    print(f'Searching urls from -> {playlist_name} playlist\nPlaylist: {i}/{n_playlists - 1}')
    print(playlist_url)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_youtube_playlist(playlist_url,playlist_name,path_save_links))

