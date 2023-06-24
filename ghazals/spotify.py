import base64
import requests
import json
from difflib import SequenceMatcher
import xlwings as xw

client_id = "7b1125ce350042c8a97b35bac9c7cfb2"
client_secret = "db34b15c8341441787f7d1df7c337d34"

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    res = requests.post(url, headers=headers, data=data)
    res = json.loads(res.content)
    token = res["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def similar(a, b):
    a = a.lower()
    b = b.lower()
    # print(b)
    return SequenceMatcher(None, a, b).ratio()

def search_spotify(token, ghazal):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"{url}?q={ghazal.replace(' ', '%20')}&type=track&limit=20"
    res = requests.get(query, headers=headers)
    res = json.loads(res.content)
    ghazals = []
    artists = []
    for track in res['tracks']['items']:
        if similar(track['name'], ghazal) < 0.65:
            continue
        ghazals.append(track["external_urls"]['spotify'])
        art = []
        for i in track['artists']:
            art.append(i['name'])
        art = ", ".join(art)
        artists.append(art)
    return [ghazals, artists]

if __name__ == "__main__":
    ghazal = "din kuchh aise guzarta hai koi"
    poet = "gulzar"
    token = get_token()
    songs = search_spotify(token, ghazal)
    excel_file = "Ghazals.xlsx"
    wb = xw.Book(excel_file)
    ws = wb.sheets['Sheet1']
    rows = ws.range('B' + str(ws.cells.last_cell.row)).end('up').row
    ws[f"A2:C{rows}"].value = ''
    ws["A2"].options(transpose=True).value = songs[0]
    ws["B2"].options(transpose=False).value = songs[1]
