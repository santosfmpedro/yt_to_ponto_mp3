import asyncio
from playwright.async_api import async_playwright
import sys
import pandas as pd 
import argparse

async def scrape_youtube_playlist(playlist_url,playlist_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(playlist_url)

        # Wait for the page to load completely (you may need to adjust the timeout)
         # Aguarde o carregamento completo da página (você pode precisar ajustar o timeout)
        await page.wait_for_selector('ytd-playlist-panel-video-renderer a.yt-simple-endpoint')

        # Extraia títulos e links dos vídeos
        video_elements = await page.query_selector_all('ytd-playlist-panel-video-renderer a.yt-simple-endpoint')
        
        playlist_data = []

        for video_element in video_elements:
            title_element = await video_element.query_selector('span.style-scope.ytd-playlist-panel-video-renderer')
           
           # title = await title_element.inner_text()
            link = await video_element.get_attribute('href')
            print(link)
            playlist_data.append({ 'link': link}) #'title': title,

        await browser.close()

        # Create a DataFrame from the playlist_data
        df = pd.DataFrame(playlist_data)

        # Save the DataFrame to a CSV file
        df.to_csv(f'{playlist_name}.csv', index=False, encoding='utf-8')

        return df

# loop = asyncio.get_event_loop()

# Extract the playlist name from the URL

# if __name__ == "__main__":
#     # Crie um argumento para o URL da playlist
#     parser = argparse.ArgumentParser(description='YouTube Playlist Scraper')
#     parser.add_argument('guide_playlist_path', type=str, help='guide_playlist Path ')
#     args = parser.parse_args()

#     guide_playlist_path = args.guide_playlist_path

import os 

print(os.getcwd())

guide_playlist_path = 'D:\PEDRO\projects\github\yt_to_ponto_mp3\guide_playlist.csv'

playlists = pd.read_csv(guide_playlist_path)

n_playlists = len(playlists) 

for i in range(n_playlists):
    if playlists['nome'][i] == None:
        playlist_name = f'playlist_{[i]}'
    else:
        playlist_name = playlists['nome'][i]
        
    playlist_url = playlists['playlist'][i]
    print(f'Searching urls from -> {playlist_name} playlist\nPlaylist: {i}/{n_playlists - 1}')
    print(playlist_url)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_youtube_playlist(playlist_url,playlist_name))


# Extrair o nome da playlist a partir da URL
playlist_name = playlist_url.split('list=')[-1]

print(f'Arquivo CSV "{playlist_name}.csv" criado com links dos vídeos.')