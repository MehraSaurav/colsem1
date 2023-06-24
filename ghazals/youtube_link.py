from difflib import SequenceMatcher
import requests

# api_key = 'AIzaSyA3_V1inlGU_fXwdy9OytoOGeP7xAbn6Zw'
# api_key = 'AIzaSyACazqHg7AyJfZzrs-IqkviFwatb-R20uE'
api_key = 'AIzaSyCYVmth3Qne2D6yLuZSjdjWChkCmrnNDGQ'

def similar(a, b):
    a = a.lower()
    b = b.lower()
    # print(b)
    return SequenceMatcher(None, a, b).ratio()

def youtube_links(poet, ghazal, api_key):
    l = len(ghazal)
    query = ghazal.replace(" ", "+") + "+" + poet.replace(" ", "+")
    req = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={query}&key={api_key}&type=video')
    # print(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={query}&key={api_key}')
    if req.status_code == 403:
        return ["Quote exceeded"]
    else:
        req = req.json()['items']
        videos = []
        for video in req:
            video_id, title = video['id']['videoId'], video['snippet']['title']
            similarity = similar(ghazal, title)
            for i in range(l, len(title) + 1):
                similarity = max(similarity, similar(ghazal, title[i - l: i + 1]))
            if similarity >= 0.6:
                videos.append(f"https://www.youtube.com/watch?v={video_id}")
        return videos

if __name__ == "__main__":
    ghazal = "din kuchh aise guzarta hai koi"
    poet = "gulzar"
    youtube_links(poet, ghazal)