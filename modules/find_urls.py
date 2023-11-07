import asyncio
from playwright.async_api import async_playwright
import sys
import pandas as pd 
import argparse

async def scrape_youtube_playlist(playlist_url):
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
            playlist_data.append({ 'link': link})#'title': title,

        await browser.close()

        playlist_name = playlist_url.split('list=')[-1]

        # Create a DataFrame from the playlist_data
        df = pd.DataFrame(playlist_data)

        # Save the DataFrame to a CSV file
        df.to_csv(f'{playlist_name}.csv', index=False, encoding='utf-8')

        return df

loop = asyncio.get_event_loop()

# Extract the playlist name from the URL

if __name__ == "__main__":
    # Crie um argumento para o URL da playlist
    parser = argparse.ArgumentParser(description='YouTube Playlist Scraper')
    parser.add_argument('playlist_url', type=str, help='URL da playlist do YouTube')
    args = parser.parse_args()

    playlist_url = args.playlist_url

    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_youtube_playlist(playlist_url))

    # Extrair o nome da playlist a partir da URL
    playlist_name = playlist_url.split('list=')[-1]

    print(f'Arquivo CSV "{playlist_name}.csv" criado com links dos vídeos.')