from bs4 import BeautifulSoup
import re
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

distribution_services = ["Steam", "Humble"]

#-----------------------------------------STEAM-----------------------------------------------------------
steam_base_url = "https://store.steampowered.com/search/?term="
steam_preference_key = "&ignore_preferences=1"
steam_search_filter = "app"
#-----------------------------------------Humble_Bundle---------------------------------------------------
humble_base_url = "https://www.humblebundle.com/store/search?sort=bestselling&search="
humble_preference_key = ""
humble_search_filter = "/store/"
title_input = input("Enter the title of a Game you want to compare prices for: ")


def web_scraper(distribution, preferences, base_url, search_filter):
    if distribution == "Steam":
        searched_url = base_url + title_input.replace(" ", "+") + preferences
        search_page = requests.get(searched_url)
        soup = BeautifulSoup(search_page.content, "lxml")

    elif distribution == "Humble":
        searched_url = base_url + title_input.replace(" ", "%20") + preferences
        url = searched_url
        chrome_executable_path = r"C:\Users\gavin\AppData\Local\Programs\Python\Python37-32\Scripts\chromedriver"
        options = Options()
        browser = webdriver.Chrome(executable_path=chrome_executable_path, options=options)
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        humble_gamepage_ending = soup.find("a", class_="entity-link js-entity-link").get("href")
        humble_gamepage_link = "https://www.humblebundle.com" + humble_gamepage_ending

        browser.get(humble_gamepage_link)
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        browser.close()

    if distribution == "Steam":
        clickables = soup.find_all("a", href=re.compile(search_filter))
        j = 0
        gameurl_list = []
        for i in clickables:
            gameurl_list.append(i.attrs["href"])
            j += 1
            if j >= 30:
                break
        try:
            first_link_found = gameurl_list[0]
        except IndexError:
            print("No game of this title found")
            quit()

        source = requests.get(first_link_found)
        soup = BeautifulSoup(source.content, "lxml")
                                                    #link
        gamepage_link = first_link_found
                                                    #title
        game_title = soup.title.text
                                                    #cost
        try:
            game_cost_sale = None
            game_cost = None

            cost = soup.find("div", class_="game_purchase_price price").text
            game_cost = cost.strip()

            cost = soup.find("div", class_="discount_final_price").text
            game_cost_sale = cost.strip()
        except AttributeError:
            print("Cant find Cost")

                                                    #summary
        try:
            game_summary = soup.find("div", class_="game_description_snippet").text
            game_summary = game_summary.strip()
        except AttributeError:
            print("No Summary")

    elif distribution == "Humble":
                                                    #link
        gamepage_link = humble_gamepage_link
                                                    #title
        game_title = soup.find("h1").text
                                                    #cost
        try:
            cost = soup.find("span", class_="current-price").text
            game_cost = cost
        except AttributeError:
            print("Cant find Cost")
        game_cost_sale = None
                                                    #summary
        try:
            game_summary = soup.find("div", class_="js-property-content property-content").text
            game_summary = game_summary.strip()
            game_summary = game_summary
        except AttributeError:
            print("No Summary")
    return game_title, game_cost, gamepage_link, game_summary, game_cost_sale



#-------------------------------------Excel(Steam, Humble Bundle)---------------------------------

def main():
    steam_game_title, steam_game_cost, steam_gamepage_link, steam_game_summary, steam_game_cost_sale = web_scraper(distribution_services[0], steam_preference_key, steam_base_url, steam_search_filter)
    humble_game_title, humble_game_cost, humble_gamepage_link, humble_game_summary, humble_game_cost_sale = web_scraper(distribution_services[1], humble_preference_key, humble_base_url, humble_search_filter)

    with open("{} Prices Compared.csv".format(title_input), "w", newline="") as csvfile:
        writer = csv.writer(csvfile, dialect="excel")
        writer.writerow(["FORMAT THE TEXT IN EXCEL FOR EASE OF USE: Wrap text then set column width to ~30, then use Autofit Height"])
        writer.writerow(["Vendor", "Title", "Price", "Link", "Summary", "If steam price is wrong, this is the discounted sale price"])
        writer.writerow([distribution_services[0], steam_game_title, steam_game_cost, steam_gamepage_link, steam_game_summary, steam_game_cost_sale])
        writer.writerow([distribution_services[1], humble_game_title, humble_game_cost, humble_gamepage_link, humble_game_summary, humble_game_cost_sale])
    csvfile.close()


main()
