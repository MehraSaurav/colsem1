from youtube_link import youtube_links
from spotify import get_token
from spotify import search_spotify
from Get_Ghazals import get_ghazal
from youtube_link_from_rekhta import youtube_link_from_rekhta
import xlwings as xw
import pandas as pd
import requests
from bs4 import BeautifulSoup

poet_name = input()
excel_file = "Ghazals.xlsx"
wb = xw.Book(excel_file)
ws = wb.sheets['Sheet1']
ws2 = wb.sheets['Sheet2']
rows = max(2, ws.range('B' + str(ws.cells.last_cell.row)).end('up').row, ws.range('A' + str(ws.cells.last_cell.row)).end('up').row)
rows2 = max(2, ws2.range('B' + str(ws2.cells.last_cell.row)).end('up').row, ws2.range('A' + str(ws2.cells.last_cell.row)).end('up').row)
ws[f"A2:E{rows}"].value = ''
ws[f"A2:C{rows}"].color = None
ws2[f"A2:C{rows2}"].value = ''
curr_row = 2
curr_row2 = 2

ghazals = get_ghazal(poet_name)
token = get_token()

api_key = "AIzaSyCYVmth3Qne2D6yLuZSjdjWChkCmrnNDGQ"
# api_key = "AIzaSyAyufVKvAfR9w6G4PFh4fkcKVmIbNjgJlM"
# api_key = "AIzaSyDoemXcnkvU5RZb_bFcSyE1e3HlN1Dpc7c"

number_of_ghazals = len(ghazals)
print(f"{number_of_ghazals} ghazals found")
count = 0

for ghazal in ghazals:
    ghazals[ghazal]["Rekhta Youtube Links"] = youtube_link_from_rekhta(ghazals[ghazal]["Rekhta Link"])
    ghazals[ghazal]["Youtube Links"] = youtube_links(poet_name, ghazal, api_key)
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
    count += 1
    ws2[f"A{curr_row2}"].value = ghazal
    ws2[f"B{curr_row2}"].options(transpose=True).value = list(ghazals[ghazal]["Rekhta Youtube Links"].keys())
    ws2[f"C{curr_row2}"].options(transpose=True).value = list(ghazals[ghazal]["Rekhta Youtube Links"].values())
    curr_row2 += max(len(ghazals[ghazal]["Rekhta Youtube Links"]), 1)
    print(f"{count} of {number_of_ghazals}")

youtube_list = ws[f"B2:B{curr_row}"].value
rekhta_list = ws2[f"B2:B{curr_row2}"].value
for i in range(0, len(youtube_list)):
    if youtube_list[i] != None and "youtube" in youtube_list[i]:
        link = youtube_list[i].split("?v=")
        link = "https://youtube.com/watch?v=" + link[1]
        if link in rekhta_list:
            ws[f"B{i + 2}"].color = (73, 235, 95)
