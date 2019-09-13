from bs4 import BeautifulSoup
from selenium import webdriver
from HotspotResults import *
from time import sleep
from statistics import mean
import re

prev_result_set = set()



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

def get_most_recent_draw(all_results, spot_dict, range_set):

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
    draw_num = int(draw_num.string)
    bonus_spot = soup.find("li", class_=re.compile("win bonus show*"))
    bonus_spot = int(bonus_spot.string)

    spot_list = []
    spot_set = set()

    for spot in winning_spots:
        spot_int = int(spot.string)
        spot_list.append(int(spot.string))
        spot_set.add(int(spot.string))

    print(spot_list)
    print(draw_num)
    print(bonus_spot)
    print(spot_set)

    #keep track of avg of nums played
    all_results.append(mean(spot_list))

    #keep sets for prev results
    #check percent change between winning numbers
    #nums_not_played_set = range_set - spot_set
    if len(prev_result_set) == 0:
        print(prev_result_set)
        prev_result_set = spot_set
        print(prev_result_set)
    else:
        nums_not_played_last_set = range_set - prev_result_set

        #intersect with current draw to find common nums
        #return perecentage oxf draw numbers for this set that did not occur
        #in last drawing
        common_nums = nums_not_played_last_set.intersection(spot_set)
        percent_common = len(common_nums) / float(len(nums_not_played_last_set))
        percent_common_list.append(percent_common)
        print("Percent common with non winners from last result set:")
        print(percent_common)

        prev_result_set = spot_set




    driver.quit()

def wait_n_minutes(n):
    sleep(60 * n)

if __name__ == '__main__':
    #list to hold all results
    all_results = []

    #map for historgram of numbers
    spot_dict = {}

    #keep track of the percent of common numbers between the
    #unchosen numbers of previous draw and numbers of current draw





    #get most recent draws and save results
    try:

        while(1):
            get_most_recent_draw(all_results, spot_dict, range_set)
            wait_n_minutes(4)

    except Exception as e:
        print(e)

    finally:
        print("Overall avg: " + str(mean(all_results)))
        print('\n\n')
        print(spot_dict)
        print('\n\n')
        print(percent_common_list)
        print('\n\n')
        print("Avg percent common: " + mean(percent_common_list))
