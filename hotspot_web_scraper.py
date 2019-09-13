import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from datetime import timedelta
from HotspotResults import *
import re
from sys import argv
from sys import exc_info
from time import sleep

NUM_PLAYS_PER_DAY = 300

#init date to be able to get next draw numbers
INIT_DATE = date(2019, 3, 1)
INIT_DRAW_NUMBER = 2475236


def get_average_of_all_results(all_results):
    avg_over_all = 0
    avg_std_dev = 0
    avg_variance = 0
    avg_median = 0
    avg_distance = 0

    for result in all_results:
         avg_over_all += result.avg
         avg_std_dev += result.std_dev
         avg_variance += result.variance
         avg_median += result.median
         avg_distance += result.avg_distance

    return {
    'avg_over_all' : avg_over_all/len(all_results),
    'avg_std_dev' : avg_std_dev/len(all_results),
    'avg_variance' : avg_variance/len(all_results),
    'avg_median' : avg_median/len(all_results),
    'avg_distance' : avg_distance/len(all_results),
    }

def date_to_draw_number(date):
    """
    Convert date to a draw number
    Input: date object
    output: first draw of specified date if exists
    """

    today = date.today()

    #hotspot plays only last for 180 days
    #validate entered date
    if (today - date).days > 180 or date > today:
        return 0

    days_between = (date - INIT_DATE).days

    return INIT_DRAW_NUMBER + (300 * days_between)


def get_results_from_draw_num(results, spot_dict, all_results):
    """
    Uses draw number to make request to lotto page for draw number
    input: draw number
    """
    url = "https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw="
    url += str(results.draw_num)
    print(url)
    response = requests.get(url)

    #create BeautifulSoup object to parse winning numbers
    soup = BeautifulSoup(response.text, "html.parser")
    spot_wins = soup.find_all("li", class_=re.compile("spot win*"))

    #all spots are li elemens
    #parse out spot number
    spot_list = []

    for i in range(len(spot_wins)):
        spot = int(spot_wins[i].string)
        spot_list.append(spot)

        if not spot in spot_dict:
            spot_dict[spot] = 1
        else:
            spot_dict[spot] += 1

        #increment pairs
        j = i + 1
        for j in range(len(spot_wins)):
            spot_j = int(spot_wins[j].string)
            if (spot, spot_j) not in pair_dict:
                pair_dict[spot, spot_j] = 1
            else:
                pair_dict[spot, spot_j] += 1

    results.set_spot_list(spot_list)

    #set bonus
    results.set_bonus(int(soup.find("li", class_="spot win bonus").string))

    print(results)

    #save results
    all_results.append(results)

def get_past_draws(start_date, num_draws, spot_dict, all_results):
    """
    Start at date 03/01/2019
    start draw: 2475236
    end draw: 2475535

    loops through all draws for the day
    """
    #validate the start_date and get draw num
    draw_num = date_to_draw_number(start_date)

    if draw_num <= 0:
        print("Error: Date entered is invalid. Dates must be at most 180 days away and must not exceed current date")

    else:
        #we have a valid draw number
        #get results
        try:
            for i in range(num_draws):
                #result object to hold all stats for current draw
                print(i)
                results = HotspotResults()
                results.set_date(start_date)
                results.set_draw_num(draw_num)

                draw_num += 1

                print("Getting results...")
                get_results_from_draw_num(results, spot_dict, all_results)

                #increment dates
                if i != 0 and i % 300 == 0:
                    start_date = start_date + timedelta(days=1)

        except:
            e = exc_info()[0]
            print(e)
            print("An error has occurred while getting results.")
            print("Last draw: " + str(draw_num))

def write_results_to_file(f_name):
    f = open(f_name, "w+")

    for result in all_results:
        f.write(str(result))

    f.close()

def get_most_recent_draw():

    url = "https://www.calottery.com/play/draw-games/hot-spot"
    print("Getting current draw...")

    #get current draws using selenium
    #need to wait on webcontent to load
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    driver = webdriver.Chrome("/Users/shaheryariqbal/bin/chromedriver", options=options)

    driver.get(url)

    #wait for webcontent to load
    sleep(5)

    #create BeautifulSoup object to parse winning numbers
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # get all spots for current draw
    winning_spots = soup.findAll("li", class_= re.compile("win (.*)show"))
    draw_num = soup.find("h3", id="hotspot-current-draw-number")
    draw_num = draw_num.string
    bonus_spot = soup.find("li", class_=re.compile("win bonus show*"))
    bonus_spot = bonus_spot.string

    spot_list = []
    spot_set = set()

    for spot in winning_spots:
        spot_list.append(int(spot.string))
        spot_set.add(int(spot.string))

    print(spot_list)
    print(draw_num)
    print(bonus_spot)

    #keep sets for prev results
    #check percent change between winning numbers
    #nums_not_played_set = range_set - spot_set
    if len(prev_result_set) == 0:
        prev_result_set = spot_set
    else:
        nums_not_played_last_set = range_set - prev_result_set

        #intersect with current draw to find common nums
        #return perecentage of draw numbers for this set that did not occur
        #in last drawing
        common_nums = nums_not_played_last_set.intersection(spot_set)
        percent_common = len(common_nums) / float(len(nums_not_played_last_set))
        percent_common_list.append(percent_common)
        print("Percent common with non winners from last result set:")
        print(percent_common)




    driver.quit()


if __name__ == "__main__":

    #list to hold all results
    all_results = []

    #map for historgram of numbers
    spot_dict = {}

    #map for historgram of most common pairs
    pair_dict = {}

    #set for set operations
    #from 1-80
    range_set = set()
    for i in range(81):
        range_set.add(i)

    prev_result_set = set()

    #keep track of percent change in the not winning set of previous draw
    #to the winning set of current draws
    percent_common_list = []

    if len(argv) == 1:
        try:
            while(1):
                get_most_recent_draw()

                #sleep for 4 minutes to wait next draw
                sleep(60 * 4)
        finally:
            #save avg of avgs
            stats_dict = get_average_of_all_results()
            print(stats_dict)
            f_name = "sample_stats.txt"
            f = open(f_name)
            f.write(str(stats_dict))
            f.close()

            #print historgram
            for i in range(81):
                if i in spot_dict:
                    print(i, spot_dict[i])
                else:
                    print("%d does not appear in spot dictionary" %(i))

            print(percent_common_list)

    else:
        try:
            print("Enter start date to start data collection...")
            year = input("Enter year: ")
            month = input("Enter month: ")
            day = input("Enter day: ")
            num_draws = input("How many draws: ")

            if(not year):
                year = 2019
            if(not month):
                month = 5
            if(not day):
                day = 1
            if(not num_draws):
                num_draws = 80

            #start scraping
            start_date = date(int(year), int(month), int(day))
            get_past_draws(start_date, int(num_draws))

        finally:
            #save avg of avgs
            stats_dict = get_average_of_all_results()
            print(stats_dict)
            f_name = "sample_stats.txt"
            f = open(f_name, 'w+')

            for stat in stats_dict:
                print(stat)
                f.write(str(stat) + ": " + str(stats_dict[stat]) + "\n")

            #print historgram
            for i in range(81):
                if i in spot_dict:
                    print(i, spot_dict[i])
                    f.write(str(i) + ": " + str(spot_dict[i]) + "\n")
                else:
                    print("%d does not appear in spot dictionary" %(i))

            #print pair histogram
            for pair_key in pair_dict:
                print(pair_key, str(pair_dict[pair_key]))
                f.write(str(pair_key) + ": " + str(pair_dict[pair_key]) + "\n")
