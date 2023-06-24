from Get_Ghazals import get_ghazal
import requests
from bs4 import BeautifulSoup

def get_youtube_link(ghazal_link):
    req = requests.get(ghazal_link)
    soup = BeautifulSoup(req.content, "html.parser")
    tag = soup.find('div', class_="videoListItem clearfix")
    try:
        link = tag.find('img').get("src")
        link = link.replace("vi/", "watch?v=")
        link = link.replace("img.", "")
        link = link[::-1]
        i = link.index("/")
        link = link[i + 1:]
        link = link[::-1]
        return link
    except:
        return ''

if __name__ == "__main__":
    poet_name = input()
    ghazals = get_ghazal(poet_name)
    for ghazal in ghazals:
        ghazals[ghazal]["Youtube Links"] = [get_youtube_link(ghazals[ghazal]["Rekhta Link"])]
        print(ghazal)
        print(ghazals[ghazal])