from Get_Ghazals import get_ghazal
import requests
from bs4 import BeautifulSoup

def youtube_link_from_rekhta(ghazal_link):
    req = requests.get(ghazal_link)
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.find_all('div', class_="videoListItem clearfix")
    youtube_links = {}
    for tag in tags:
        youtube_links[f"https://www.youtube.com/watch?v={tag['data-id']}"] = tag['data-desc']
    return youtube_links

if __name__ == "__main__":
    poet_name = input()
    ghazals = get_ghazal(poet_name)
    for ghazal in ghazals:
        ghazals[ghazal]["Rekhta Youtube Links"] = youtube_link_from_rekhta(ghazals[ghazal]["Rekhta Link"])
        print(ghazal)
        print(ghazals[ghazal])
