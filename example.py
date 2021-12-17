import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/title/tt0944947/?ref_=nv_sr_srsg_0'

html_page = requests.get(url).text

soup = BeautifulSoup(html_page, 'html.parser')

title = soup.find('h1', class_="TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG").text

sections = soup.findAll('a', class_="ipc-title ipc-title--section-title ipc-title--base ipc-title--on-textPrimary ipc-title-link-wrapper")
episodes_url = sections[0].get('href')
videos_url = sections[1].get('href')

print(title)
print('Done')
