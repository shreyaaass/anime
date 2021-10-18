import os
os.system("pip install requests bs4")
os.system("cls")
import requests
from bs4 import BeautifulSoup

url="https://tenshi.moe"

anime_input = input("Enter anime you want to watch: ")
anime_input = "+".join(anime_input.split())

search_page = url + "/anime?q=" + anime_input
s = requests.get(search_page).text

soup = BeautifulSoup(s, 'lxml')
anime_titles = soup.findAll('span', {'class':'text-primary'})
anime_links = soup.findAll('a', href=True)

if len(anime_titles) == 0:
    print("No anime found")
    exit(1)

print("Available Anime: ")
c = 1
for i in anime_titles:
    print(c, ">", i.text) 
    c+=1
# stores links of the displayed animes
anime_list = []
for i in anime_links:
    if len(i['href']) == 33 and "https://tenshi.moe/anime/" in i['href']:
        anime_list.append(i['href'])

print("\nEnter which one u wanna watch: ")
n = int(input())
if n>len(anime_list):
    print("Out of range")
    exit(1)
to_watch_link = anime_list[n-1]


print("Which episode?: ")
ep = int(input())
epilink = to_watch_link + "/" + str(ep)
fname = "_".join(anime_titles[n-1].text.split()) + "_Ep" + str(ep) + ".mp4"

soup = BeautifulSoup(requests.get(epilink).text, 'lxml')
if soup.find('title').text == "404 Not Found — tenshi.moe":
    print("Out of range")
    exit(1)


url = soup.find('meta', {'property': 'og:url'})['content']
url = url[url.find('=') + 1:]

to = f'https://tenshi.moe/embed?v={url}'

# to find the download link since it is inside a js file which is unparseable
r = requests.get(to)
soup = BeautifulSoup(r.text, features = 'lxml')
text_with_link = soup.findAll('script')[3]
download_link = text_with_link.text.split()[38]
download_link = download_link[1:-2]

print("do you want to download or stream? (choose 1/2)")
op = int(input())
while(op<=2 and op>0):
    if op == 1:
        os.system("curl {0} -o {1}".format(download_link, fname))
        break
    else:
        os.system("vlc {0}".format(download_link))
        break
