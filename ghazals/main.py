from youtube_link import youtube_links
from spotify import get_token
from spotify import search_spotify
from Get_Ghazals import get_ghazal
from youtube_link_from_rekhta import get_youtube_link
import xlwings as xw
import requests
from bs4 import BeautifulSoup

poet_name = input("Enter the name of the artist:")
excel_file = "Ghazals.xlsx"
wb = xw.Book(excel_file)
ws = wb.sheets['Sheet1']
rows = ws.range('B' + str(ws.cells.last_cell.row)).end('up').row
ws[f"A2:C{rows}"].value = ''
curr_row = 2
ws["A1"].value = ["Ghazal", "Link", "Artist"]

ghazals = get_ghazal(poet_name)
token = get_token()

# api_key = "AIzaSyCYVmth3Qne2D6yLuZSjdjWChkCmrnNDGQ"
# api_key = "AIzaSyAyufVKvAfR9w6G4PFh4fkcKVmIbNjgJlM"
api_key = "AIzaSyDoemXcnkvU5RZb_bFcSyE1e3HlN1Dpc7c"

for ghazal in ghazals:
    ghazals[ghazal]["Youtube Links"] = [get_youtube_link(ghazals[ghazal]["Rekhta Link"])]
    ghazals[ghazal]["Youtube Links"] += youtube_links(poet_name, ghazal, api_key)
    if '' in ghazals[ghazal]["Youtube Links"]:
        ghazals[ghazal]["Youtube Links"].remove('')
    ghazals[ghazal]["Spotify Links"] = search_spotify(token, ghazal)
    ws[f"A{curr_row}"].value = ghazal
    ws[f"B{curr_row}"].options(transpose=True).value = ghazals[ghazal]["Youtube Links"]
    curr_row += len(ghazals[ghazal]["Youtube Links"])
    ws[f"B{curr_row}"].options(transpose=True).value = ghazals[ghazal]["Spotify Links"][0]
    ws[f"C{curr_row}"].options(transpose=True).value = ghazals[ghazal]["Spotify Links"][1]
    curr_row += len(ghazals[ghazal]["Spotify Links"][0])
    if len(ghazals[ghazal]["Youtube Links"]) + len(ghazals[ghazal]["Spotify Links"][0]) == 0:
        curr_row += 1