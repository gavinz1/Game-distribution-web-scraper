from bs4 import BeautifulSoup
import re
import requests
import csv

#the goal is to make a program that takes a game name as an input and prints a bunch of useful information in title, cost, summary, and the link to the page to help inform buying.

game_title = input("Enter the title of a Game you want to compare prices for: ")
distribution_services = ["Steam"]
#-----------------------------------------STEAM-----------------------------------------------------------
steam_base_search_url = "https://store.steampowered.com/search/?term="
steam_searched_url = steam_base_search_url + game_title.replace(" ", "+") + "&ignore_preferences=1"
print(steam_searched_url)

steam_search_page = requests.get(steam_searched_url)
soup = BeautifulSoup(steam_search_page.content, "lxml")

clickables = soup.find_all("a", href=re.compile("app"))

j = 0
steam_games = []
steam_app_identify = "https://store.steampowered.com/app/"

for i in clickables:
    steam_games.append(i.attrs["href"])
    j += 1
    if j >= 30:
        break

try:
    steam_link = steam_games[0]
except IndexError:
    print("No game of this title found")
    quit()

source = requests.get(steam_link)
soup = BeautifulSoup(source.content, "lxml")

                                        #link
print(steam_link)
                                        #title
steam_title = soup.title.text
print(steam_title)
                                        #cost

try:
    cost = soup.find("div", class_="game_purchase_price price").text
    steam_cost = cost.strip()
    print(steam_cost)

    cost = soup.find("div", class_="discount_final_price").text
    steam_cost_sale = cost.strip()
    print(steam_cost_sale)



except AttributeError:
    print("Cant find Cost")
    quit()


                                        #summary
try:
    steam_summary = soup.find("div", class_="game_description_snippet").text
    steam_summary = steam_summary.strip()
    print(steam_summary)
except AttributeError:
    print("No Summary")

#-------------------------------------Excel(Steam, )---------------------------------
with open("{} Prices Compared.csv".format(game_title), "w", newline="") as csvfile:
    writer = csv.writer(csvfile, dialect="excel")
    writer.writerow(["FORMAT THE TEXT IN EXCEL FOR EASE OF USE: Wrap text then set column width to ~30, then use Autofit Height"])
    writer.writerow(["Title", "Price", "Link", "Summary", "If price is wrong, this is the discounted sale price"])
    writer.writerow([steam_title, steam_cost, steam_link, steam_summary, steam_cost_sale])
csvfile.close()
