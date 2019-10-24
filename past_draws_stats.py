from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from datetime import date
from datetime import timedelta
from statistics import mean

import init_functions as init
import file_writing_funcs as write
import data_tracker_funcs as data_tracker

import re
import json
import requests
import sys
import os
import json

import drawing_set_stats as dss

last_n = 15

NUM_SPOTS_PLAYED = 20
NUM_LOSING_SPOTS = 60
NUM_DRAWINGS_PER_DAY = 300


#init date to be able to get next draw numbers
INIT_DATE = date(2019, 3, 1)
INIT_DRAW_NUMBER = 2475236

#hold results of
current_cached_file = None
#dict will hold draw nums for current cached file
current_cached_draw_nums = None

next_day_draws_dict = None
next_day_draws_f_name = None

#hold the dictionary for most recent spot that was selected
#
# current_draw_num_dict
#
# def check_draw_num_cached(draw_num):
def cache_draw_result(draw_num, winning_spots_list):
    global next_day_draws_dict
    global next_day_draws_f_name

    if(next_day_draws_dict is None):
        #cache draw result
        print("Caching draw result...")

        next_day_draws_dict = {draw_num : winning_spots_list}
        next_day_draws_f_name = str(draw_num_to_date(draw_num)) + "_winning_sets.json"
    else:
        #check if same date
        date_f_name =  str(draw_num_to_date(draw_num)) + "_winning_sets.json"

        if(date_f_name == next_day_draws_f_name):
            next_day_draws_dict[draw_num] = winning_spots_list
        else:
            #next day has started
            #save file
            write.write_dict_to_file(next_day_draws_dict, "winning_spots/" + next_day_draws_f_name)
            next_day_draws_dict = {draw_num : winning_spots_list}
            next_day_draws_f_name = date_f_name

def get_cached_draw_result(draw_date, draw_num):
    """
    Given a draw date and draw number, will open
    return dict of
    """
    global current_cached_file
    global current_cached_draw_nums
    global next_day_draws_f_name

    if(current_cached_draw_nums is not None):
        if(str(draw_num) in current_cached_draw_nums.keys()):
            return

    try:

        json_file_name = "winning_spots/" + str(draw_date) + "_winning_sets.json"
        print(json_file_name)

        if(current_cached_file == json_file_name):
            #check if draw num exists in dict
            if(current_cached_draw_nums is not None and str(draw_num) in current_cached_draw_nums.keys()):
                return
            else:

                #check next file, if not found set to none
                next_date = draw_date + timedelta(days=1)
                json_file_name = "winning_spots/" + str(next_date) + "_winning_sets.json"
                json_file = open(json_file_name, "r")

                print("Draw num not found checking next draw dict...")
                print(json_file_name)

                current_cached_file = json_file_name
                current_cached_draw_nums = json.load(json_file)

                if(str(draw_num) not in current_cached_draw_nums.keys()):
                    print("Not in next day. Setting none.")
                    current_cached_file = None
                    current_cached_draw_nums = None



        # if(current_cached_file == json_file_name):
        #     print("Current file:", current_cached_file)
        #     print("Json file:", json_file_name)
        #     #already are reading from cached file
        #     return
        else:
            json_file = open(json_file_name, "r")
            current_cached_file = json_file_name
            print("New Current File:", current_cached_file)
            current_cached_draw_nums = json.load(json_file)

    except FileNotFoundError:
        #if file does not exist no cached draw nums, use beutiful soup
        current_cached_file = None
        current_cached_draw_nums = None
        print("File not found")
        return


def draw_num_to_date(draw_num):
    """
    Convert draw num to date object of date that draw_num played
    return date(year, month, day) object
    """

    #each day 300 draws, find diff in draw num from init draw num
    draw_diff = draw_num - INIT_DRAW_NUMBER + 1
    days_diff = draw_diff / 300

    draw_num_date = INIT_DATE + timedelta(days=days_diff)

    #add date by days diff
    print("Draw num:", draw_num, "Date:", draw_num_date)
    return draw_num_date


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


    # num_spots_sampled, spot_histogram, range_histogram, mod_histogram,
    #     last_seen_dict, avg_draw_distance_dict, draw_distance_dict, last_n_avg_distance_dict_list, current_draw_num

def get_stats_from_soup_list(winning_spots_soup, current_draw_num, num_spots_sampled=None, spot_histogram=None, range_histogram=None, mod_histogram=None,
    last_seen_dict=None, avg_draw_distance_dict=None, draw_distance_dict=None, last_n_avg_distance_dict_list=None, last_n_avg_distance_dict=None):
    """
    Input beutiful soup list of li elements
    output: dict with
    ret_dict = {
        "spot_list" : spot_list,
        "spot_set" : spot_set,
        "mean" : mean,
    }
    """
    spot_list = []
    spot_set = set()

    mean = 0

    for spot in winning_spots_soup:

        spot_int = int(spot)

        spot_list.append(spot_int)
        spot_set.add(spot_int)
        mean += spot_int

        #add to historgram of nums
        if(spot_histogram is not None):
            data_tracker.increment_spot_hist(spot_histogram, spot_int)

        #add to range buckets histogram
        if(range_histogram is not None):
            data_tracker.increment_range_hist(range_histogram, spot_int)

        #add to even numbers and odd numbers count
        #add to mod 5 and mod 10 count
        #add percent of primes for current draw
        if(mod_histogram is not None):
            data_tracker.increment_mod_hist(mod_histogram, spot_int)

        #add to avg num draws between numbers selection
        if(last_seen_dict is not None
            and draw_distance_dict is not None
            and current_draw_num is not None):

                data_tracker.increment_draw_distance_sums(current_draw_num, spot_int, last_seen_dict, draw_distance_dict, avg_draw_distance_dict,
                    last_n_avg_distance_dict_list, last_n_avg_distance_dict)

        if(num_spots_sampled is not None):
            num_spots_sampled += 1


    mean /= float(NUM_SPOTS_PLAYED)

    # print(spot_set)

    ret_dict = {
        "spot_list" : spot_list,
        "spot_set" : spot_set,
        "mean" : mean,
    }

    return ret_dict




def get_results_from_draw_num(draw_num, num_spots_sampled=None, spot_histogram=None, range_histogram=None, mod_histogram=None,
    last_seen_dict=None, avg_draw_distance_dict=None, draw_distance_dict=None, last_n_avg_distance_dict_list=None,
    last_n_avg_distance_dict=None):
    """
    Uses draw number to make request to lotto page for draw number
    input: draw number
    return: dict  with
    """

    global next_day_draws_f_name
    global next_day_draws_dict


    #check if draw is cached
    get_cached_draw_result(draw_num_to_date(draw_num), draw_num)

    if(current_cached_draw_nums is None):

        #parse html page
        url = "https://www.calottery.com/draw-games/hot-spot/past-winning-numbers?query=" + str(draw_num) + "#search"
        # url = "https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw="
        # url += str(draw_num)
        print(url)
        response = requests.get(url)

        #create BeautifulSoup object to parse winning numbers
        soup = BeautifulSoup(response.text, "html.parser")
        winning_spots = soup.find_all("li", class_=re.compile("list-inline-item (blue|yellow)-num*"))

        winning_spots = [int(x.string) for x in winning_spots]
        print(winning_spots)

        cache_draw_result(draw_num, winning_spots)

    else:
        print("Getting cached results...")
        winning_spots = current_cached_draw_nums[str(draw_num)]

    return get_stats_from_soup_list(winning_spots, draw_num, num_spots_sampled, spot_histogram, range_histogram, mod_histogram,
        last_seen_dict, avg_draw_distance_dict, draw_distance_dict, last_n_avg_distance_dict_list, last_n_avg_distance_dict)

def get_most_recent_draw(num_spots_sampled=None, spot_histogram=None, range_histogram=None, mod_histogram=None,
    last_seen_dict=None, avg_draw_distance_dict=None, draw_distance_dict=None, last_n_avg_distance_dict_list=None,
    last_n_avg_distance_dict=None, first_draw=False):
    """
    Input: None
    Output: Python dict with winning numbers
    {
        spot_list :
        spot_set :
        mean :
    }
    """
    url = "https://www.calottery.com/play/draw-games/hot-spot"
    # print("Getting current draw...")
    #
    # #get current draws using selenium
    # #need to wait on webcontent to load
    # options = webdriver.ChromeOptions()
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--incognito")
    # options.add_argument("--headless")
    # driver = webdriver.Chrome("/Users/shaheryariqbal/bin/chromedriver", options=options)
    #
    # driver.get(url)
    #
    # #wait for webcontent to load
    # sleep(7)

    url = "https://www.calottery.com/draw-games/hot-spot"
    # url = "https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw="
    # url += str(draw_num)
    print(url)
    response = requests.get(url)


    #create BeautifulSoup object to parse winning numbers
    soup = BeautifulSoup(response.text, "html.parser")

    # get all spots for current draw
    winning_spots = soup.findAll("li", class_= re.compile("list-inline-item (blue|yellow)-num*"))
    winning_spots = [int(x.string) for x in winning_spots]
    draw_num = soup.findAll("strong", class_="current-drawNumber")[0]
    draw_num = int(draw_num.string)

    print(draw_num)
    print(winning_spots)

    cache_draw_result(draw_num, winning_spots)

    # driver.quit()

    #if first draw init last_seen_dict
    if first_draw:
        for key in last_seen_dict.keys():
            last_seen_dict[key] = draw_num


    ret_dict = get_stats_from_soup_list(winning_spots, draw_num,
        num_spots_sampled, spot_histogram, range_histogram, mod_histogram,
        last_seen_dict, avg_draw_distance_dict, draw_distance_dict, last_n_avg_distance_dict_list,
        last_n_avg_distance_dict)

    ret_dict["draw_num"] = draw_num

    return ret_dict



def wait_n_minutes(n):
    sleep(60 * n)

def prompt_for_date():
    """
    return: dict with date params
    {
    year
    month
    day
    num_days_to_sample
    start_date (date object)
    }
    """
    print("Getting past draw date...")
    # year = input("Enter year: ")
    year = 2019
    month = input("Enter month: ")
    day = input("Enter day: ")
    num_days_to_sample = input("Enter number of days to sample: ")
    sample_num = input("Enter the sample number: ")

    # if(len(year) <= 1):
    #     year = 2019

    if(len(month) < 1):
        # print("Error: Invalid month")
        # exit(0)
        month = 9

    if(len(day) < 1):
        day = 1

    if(len(num_days_to_sample) < 1):
        num_days_to_sample = 1

    if(len(sample_num) < 1):
        sample_num = 1

    ret_dict = {
        "year" : int(year),
        "month" : int(month),
        "day" : int(day),
        "num_days_to_sample" : int(num_days_to_sample),
        "sample_num" : int(sample_num),
        "start_date" : date(int(year), int(month), int(day)),
    }

    return ret_dict

if __name__ == "__main__":
    # draw_num_to_date(2544516)

    # get_results_from_draw_num(2544516)
    get_most_recent_draw()

    # #historgram for # numbers in draws that are evenly divisible by dict keys
    # mod_histogram = {
    #     "odd" : 0,
    #     "even" : 0,
    #     3 : 0,
    #     5 : 0,
    #     10 : 0,
    #     "end_in_0" : 0,
    #     "end_in_1" : 0,
    #     "end_in_2" : 0,
    #     "end_in_3" : 0,
    #     "end_in_4" : 0,
    #     "end_in_5" : 0,
    #     "end_in_6" : 0,
    #     "end_in_7" : 0,
    #     "end_in_8" : 0,
    #     "end_in_9" : 0,
    # }
    #
    # #dict holds value for num of draws between when specified key was last a winning number
    # last_seen_dict = init.init_spot_dict()
    #
    # #dict holds avg num draws between spot selections
    # #keep count of sum of distances
    # #divide by total num draws
    # avg_draw_distance_dict = init.init_spot_dict()
    #
    # #dict hold for each spot a list of its
    # #draw distances
    # draw_distance_dict = init.init_spot_dict_list()
    #
    #
    # #dict of of dict lists tol for avg of last i elements in draw_distance_dict
    # #dict[spot_num][n] = list avg of last n elements of draw_distance_dict for the spot_num
    # last_n_avg_distance_dict_list = init.init_spot_dict_dict_list(last_n)
    #
    #
    # #map for historgram of numbers
    # spot_histogram = init.init_spot_dict()
    # # print(spot_histogram)
    # #buckets to count winning nums
    # range_histogram = {
    #     "1-10" : 0,
    #     "11-20" : 0,
    #     "21-30" : 0,
    #     "31-40" : 0,
    #     "41-50" : 0,
    #     "51-60" : 0,
    #     "61-70" : 0,
    #     "71-80" : 0,
    # }
    #
    # num_spots_sampled = 0
    # num_draws_sampled = 0
    # current_draw_num = 0
    # starting_draw_num = 0
    #
    # #hold list of avgs of previous draws
    # mean_list = []
    #
    # #hold list of percentage diff between losers/winners of prev draws and
    # #current draws
    # prev_result_set = set()
    # prev2_result_set = set()
    # prev3_result_set = set()
    # prev4_result_set = set()
    # prev5_result_set = set()
    # prev6_result_set = set()
    # prev7_result_set = set()
    # prev8_result_set = set()
    # prev9_result_set = set()
    # prev10_result_set = set()
    #
    # curr_result_set = set()
    #
    # #percent prev losers selected -> ppls
    # ppls_list = []
    # pp2ls_list = []
    # pp3ls_list = []
    # pp4ls_list = []
    # pp5ls_list = []
    # pp6ls_list = []
    # pp7ls_list = []
    # pp8ls_list = []
    # pp9ls_list = []
    # pp10ls_list = []
    #
    # #percent prev winners selected -> ppws
    # ppws_list = []
    # pp2ws_list = []
    # pp3ws_list = []
    # pp4ws_list = []
    # pp5ws_list = []
    # pp6ws_list = []
    # pp7ws_list = []
    # pp8ws_list = []
    # pp9ws_list = []
    # pp10ws_list = []
    #
    # #percent_selected_from_prev_losers -> psfpl
    # #list of percent composition of current winning numbers from previous losing numbers
    # psfpl_list = []
    # psfp2l_list = []
    # psfp3l_list = []
    # psfp4l_list = []
    # psfp5l_list = []
    # psfp6l_list = []
    # psfp7l_list = []
    # psfp8l_list = []
    # psfp9l_list = []
    # psfp10l_list = []
    #
    # #percent_selected_from_prev_winners -> psfpw
    # #list of percent composition of current winning numbers from previous winning numbers
    # psfpw_list = []
    # psfp2w_list = []
    # psfp3w_list = []
    # psfp4w_list = []
    # psfp5w_list = []
    # psfp6w_list = []
    # psfp7w_list = []
    # psfp8w_list = []
    # psfp9w_list = []
    # psfp10w_list = []
    #
    # #since mean for hotspot is always around 40
    # #generator will try to pick all numbers once
    # #at least every 4 draws
    #
    #
    # #list percent of winning numbers that were selected from set intersection
    # #of previous draws losers
    # #numbers that have lost twice in a row
    # #percent intersection of previous 2 losers selected = pip2ls
    # pip2ls_list = []
    # pip3ls_list = []
    # pip4ls_list = []
    # pip5ls_list = []
    # pip6ls_list = []
    # pip7ls_list = []
    # pip8ls_list = []
    # pip9ls_list = []
    # pip10ls_list = []
    #
    # #list of percent composition of winning numbers from intersection
    # #of previous draws losers
    # #percent selected from intersection of previous 2 losers -> psfip2
    # psfip2_list = []
    # psfip3_list = []
    # psfip4_list = []
    # psfip5_list = []
    # psfip6_list = []
    # psfip7_list = []
    # psfip8_list = []
    # psfip9_list = []
    # psfip10_list = []
    #
    # #list of percent of remaining_nums_set selected for current draws
    # #percent remaining nums selected -> prns
    # prns_list = []
    #
    # #list of percent composition of current draw set from remaining_nums_set
    # #percent selected from remaining_nums_set -> psfrn
    # psfrn_list = []
    #
    # #list for num draws needed before 1 round is complete
    # #one round is the num of draws needed for all nums in range
    # #1-80 to be selected as winners
    # draws_per_round_list = []
    #
    # #list for percentage of intersection of prev2 losers and remaining_nums_set selected in current draw
    # #percent intersect prev2 losers remaining nums selected ->pip2lrns
    # pip2lrns_list = []
    #
    # #list for percent composition of current draw from intersection of prev2 losers and remaining_nums_set
    # #percent selected from intersect prev2 losers remaining nums -> psfip2lrn
    # psfip2lrn_list = []
    #
    # #num draws before the last number from the current round is selected
    # draws_till_new_round_list = []
    #
    # start_date = 0
    #
    # #get continuous results
    # try:
    #     #mode 0 : get current draws
    #     #mode 1 : get past draw numbers
    #     if(len(sys.argv) == 2):
    #         #get date
    #         prompt_dict = prompt_for_date()
    #         print(prompt_dict)
    #
    #         start_date = date(prompt_dict["year"], prompt_dict["month"], prompt_dict["day"])
    #         print(start_date)
    #
    #         starting_draw_num = date_to_draw_number(start_date)
    #         current_draw_num = starting_draw_num
    #         print(current_draw_num)
    #
    #         #set last seen to current draw num
    #         last_seen_dict = init.init_spot_dict_val(starting_draw_num)
    #         # print(last_seen_dict)
    #
    #         total_num_draws_to_sample = prompt_dict["num_days_to_sample"] * NUM_DRAWINGS_PER_DAY
    #         num_draws_sampled = 0
    #
    #         while(num_draws_sampled < total_num_draws_to_sample):
    #             print(num_draws_sampled, current_draw_num)
    #
    #             # dss.print_dict(result_stats_dict)
    #
    #             result_dict = get_results_from_draw_num(current_draw_num, num_spots_sampled, spot_histogram, range_histogram, mod_histogram,
    #                 last_seen_dict, avg_draw_distance_dict, draw_distance_dict, last_n_avg_distance_dict_list)
    #
    #             mean_list.append(result_dict["mean"])
    #
    #             #conditions for first 4 draws
    #             if(num_draws_sampled <= 10):
    #                 if(num_draws_sampled == 0):
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 1):
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 2):
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 3):
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 4):
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 5):
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 6):
    #                     prev6_result_set = prev5_result_set
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #
    #                 elif(num_draws_sampled == 7):
    #                     prev7_result_set = prev6_result_set
    #                     prev6_result_set = prev5_result_set
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #                 elif(num_draws_sampled == 8):
    #                     prev8_result_set = prev7_result_set
    #                     prev7_result_set = prev6_result_set
    #                     prev6_result_set = prev5_result_set
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #                 elif(num_draws_sampled == 9):
    #                     prev9_result_set = prev8_result_set
    #                     prev8_result_set = prev7_result_set
    #                     prev7_result_set = prev6_result_set
    #                     prev6_result_set = prev5_result_set
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #                 elif(num_draws_sampled == 10):
    #                     prev10_result_set = prev9_result_set
    #                     prev9_result_set = prev8_result_set
    #                     prev8_result_set = prev7_result_set
    #                     prev7_result_set = prev6_result_set
    #                     prev6_result_set = prev5_result_set
    #                     prev5_result_set = prev4_result_set
    #                     prev4_result_set = prev3_result_set
    #                     prev3_result_set = prev2_result_set
    #                     prev2_result_set = prev_result_set
    #                     prev_result_set = curr_result_set
    #                     curr_result_set = result_dict["spot_set"]
    #             else:
    #                 #we have atleast 4 results sets to work with
    #                 #get set statistics
    #                 prev10_result_set = prev9_result_set
    #                 prev9_result_set = prev8_result_set
    #                 prev8_result_set = prev7_result_set
    #                 prev7_result_set = prev6_result_set
    #                 prev6_result_set = prev5_result_set
    #                 prev5_result_set = prev4_result_set
    #                 prev4_result_set = prev3_result_set
    #                 prev3_result_set = prev2_result_set
    #                 prev2_result_set = prev_result_set
    #                 prev_result_set = curr_result_set
    #                 curr_result_set = result_dict["spot_set"]
    #
    #                 set_stats_dict = dss.get_set_stats(current_draw_num, curr_result_set, prev_result_set, prev2_result_set,
    #                     prev3_result_set, prev4_result_set, prev5_result_set, prev6_result_set,
    #                     prev7_result_set, prev8_result_set, prev9_result_set, prev10_result_set)
    #
    #
    #                 if("draws_till_new_round" in set_stats_dict.keys()):
    #                     draws_till_new_round_list.append(set_stats_dict["draws_till_new_round"])
    #
    #                 #parse results and append to lists
    #                 dss.parse_ppls_set_stats(set_stats_dict, ppls_list, pp2ls_list, pp3ls_list, pp4ls_list,
    #                     pp5ls_list, pp6ls_list, pp7ls_list, pp8ls_list, pp9ls_list, pp10ls_list)
    #
    #                 dss.parse_ppws_set_stats(set_stats_dict, ppws_list, pp2ws_list, pp3ws_list, pp4ws_list,
    #                      pp5ws_list, pp6ws_list,  pp7ws_list, pp8ws_list,  pp9ws_list, pp10ws_list)
    #
    #                 dss.parse_psfpl_set_stats(set_stats_dict, psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list,
    #                     psfp5l_list, psfp6l_list, psfp7l_list, psfp8l_list, psfp9l_list, psfp10l_list)
    #
    #                 dss.parse_psfpw_set_stats(set_stats_dict, psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list,
    #                     psfp5w_list, psfp6w_list, psfp7w_list, psfp8w_list, psfp9w_list, psfp10w_list)
    #
    #                 dss.parse_pipls_set_stats(set_stats_dict, pip2ls_list, pip3ls_list, pip4ls_list,
    #                     pip5ls_list, pip6ls_list, pip7ls_list, pip8ls_list, pip9ls_list, pip10ls_list)
    #
    #                 dss.parse_psfip_set_stats(set_stats_dict, psfip2_list, psfip3_list, psfip4_list,
    #                     psfip5_list, psfip6_list, psfip7_list, psfip8_list, psfip9_list, psfip10_list)
    #
    #                 # dss.parse_remaining_nums_set_stats(set_stats_dict, prns_list, psfrn_list, draws_per_round_list)
    #                 # dss.parse_intersect_remaining_num_set_stats(set_stats_dict, pip2lrns_list, psfip2lrn_list)
    #
    #             num_draws_sampled += 1
    #             current_draw_num += 1
    #
    #
    #
    #
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     print(e)
    #
    # finally:
    #     #print final stats
    #     #save to all lists to files
    #     print("Last draw num: " + str(current_draw_num))
    #     #print("Starting from " + str(start_date) + " attempted to get results for " + total_num_draws_to_sample + " draws")
    #     print("Num spots sampled: " + str(num_spots_sampled))
    #     print("Num draws sampled: " + str(num_draws_sampled))
    #
    #     #get avg draw distance
    #     #avg_draw_distance_dict holds sums of distances
    #     for key in avg_draw_distance_dict.keys():
    #         # get avg by dividing the sum of draw distances / num times a num is played
    #         avg_draw_distance_dict[key] /= float(spot_histogram[key])
    #
    #     #avg draw distance for all numbers
    #     avg_draw_distance_dict["avg_over_all"] = mean(avg_draw_distance_dict.values())
    #
    #     #print all historgrams
    #     dss.print_dict(spot_histogram)
    #     dss.print_dict(range_histogram)
    #     dss.print_dict(mod_histogram)
    #
    #
    #     #print all set stats
    #     #get avg for al percent changes between losers and winners of previous sets
    #     ppls_dict = dss.get_ppls_stats(ppls_list, pp2ls_list, pp3ls_list, pp4ls_list, pp5ls_list,
    #         pp6ls_list, pp7ls_list, pp8ls_list, pp9ls_list, pp10ls_list)
    #
    #     ppws_dict = dss.get_ppws_stats(ppws_list, pp2ws_list, pp3ws_list, pp4ws_list, pp5ws_list,
    #         pp6ws_list, pp7ws_list, pp8ws_list, pp9ws_list, pp10ws_list)
    #
    #     psfpl_dict = dss.get_psfpl_stats(psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list,
    #         psfp5l_list, psfp6l_list, psfp7l_list, psfp8l_list, psfp9l_list, psfp10l_list, )
    #
    #     psfpw_dict = dss.get_psfpw_stats(psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list, psfp5w_list,
    #         psfp6w_list, psfp7w_list, psfp8w_list, psfp9w_list, psfp10w_list)
    #
    #     psfip_dict = dss.get_psfip_stats(psfip2_list, psfip3_list, psfip4_list, psfip5_list,
    #         psfip6_list, psfip7_list, psfip8_list, psfip9_list, psfip10_list)
    #
    #     pipls_dict = dss.get_pipls_stats(pip2ls_list, pip3ls_list, pip4ls_list, pip5ls_list,
    #         pip6ls_list, pip7ls_list, pip8ls_list, pip9ls_list, pip10ls_list)
    #
    #     remaining_nums_stats_dict = dss.get_remaining_nums_stats(prns_list, psfrn_list, draws_per_round_list)
    #
    #     #prev losers intersect remaining nums stats -> plirn_stats
    #     #plirn_stats = dss.get_plirn_stats(pip2lrns_list, psfip2lrn_list)
    #
    #     sample_num_str = str(prompt_dict["sample_num"])
    #
    #     #write everything to files
    #     overall_mean = mean(mean_list)
    #     write.write_mean_list_to_file(mean_list, overall_mean, "sample_means_list_sample_2.txt")
    #
    #     write.write_mean_list_to_file(ppls_list, ppls_dict["avg_ppls"], "percent_previous_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp2ls_list, ppls_dict["avg_pp2ls"], "percent_previous_2_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp3ls_list, ppls_dict["avg_pp3ls"], "percent_previous_3_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp4ls_list, ppls_dict["avg_pp4ls"], "percent_previous_4_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp5ls_list, ppls_dict["avg_pp5ls"], "percent_previous_5_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp6ls_list, ppls_dict["avg_pp6ls"], "percent_previous_6_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp7ls_list, ppls_dict["avg_pp7ls"], "percent_previous_7_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp8ls_list, ppls_dict["avg_pp8ls"], "percent_previous_8_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp9ls_list, ppls_dict["avg_pp9ls"], "percent_previous_9_losers_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp10ls_list, ppls_dict["avg_pp10ls"], "percent_previous_10_losers_selected_list_sample_" + sample_num_str + ".txt")
    #
    #     write.write_mean_list_to_file(ppws_list, ppws_dict["avg_ppws"], "percent_previous_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp2ws_list, ppws_dict["avg_pp2ws"], "percent_previous_2_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp3ws_list, ppws_dict["avg_pp3ws"], "percent_previous_3_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp4ws_list, ppws_dict["avg_pp4ws"], "percent_previous_4_winners_selected_list_sample_" + sample_num_str + "2.txt")
    #     write.write_mean_list_to_file(pp5ws_list, ppws_dict["avg_pp5ws"], "percent_previous_5_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp6ws_list, ppws_dict["avg_pp6ws"], "percent_previous_6_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp7ws_list, ppws_dict["avg_pp7ws"], "percent_previous_7_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp8ws_list, ppws_dict["avg_pp8ws"], "percent_previous_8_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp9ws_list, ppws_dict["avg_pp9ws"], "percent_previous_9_winners_selected_list_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pp10ws_list, ppws_dict["avg_pp10ws"], "percent_previous_10_winners_selected_list_sample_" + sample_num_str + ".txt")
    #
    #     write.write_mean_list_to_file(psfpl_list, psfpl_dict["avg_psfpl"], "percent_selected_from_prev_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp2l_list, psfpl_dict["avg_psfp2l"], "percent_selected_from_prev2_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp3l_list, psfpl_dict["avg_psfp3l"], "percent_selected_from_prev3_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp4l_list, psfpl_dict["avg_psfp4l"], "percent_selected_from_prev4_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp5l_list, psfpl_dict["avg_psfp5l"], "percent_selected_from_prev5_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp6l_list, psfpl_dict["avg_psfp6l"], "percent_selected_from_prev6_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp7l_list, psfpl_dict["avg_psfp7l"], "percent_selected_from_prev7_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp8l_list, psfpl_dict["avg_psfp8l"], "percent_selected_from_prev8_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp9l_list, psfpl_dict["avg_psfp9l"], "percent_selected_from_prev9_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp10l_list, psfpl_dict["avg_psfp10l"], "percent_selected_from_prev10_losers_sample_" + sample_num_str + ".txt")
    #
    #     write.write_mean_list_to_file(psfpw_list, psfpw_dict["avg_psfpw"], "percent_selected_from_prev_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp2w_list, psfpw_dict["avg_psfp2w"], "percent_selected_from_prev2_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp3w_list, psfpw_dict["avg_psfp3w"], "percent_selected_from_prev3_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp4w_list, psfpw_dict["avg_psfp4w"], "percent_selected_from_prev4_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp5w_list, psfpw_dict["avg_psfp5w"], "percent_selected_from_prev5_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp6w_list, psfpw_dict["avg_psfp6w"], "percent_selected_from_prev6_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp7w_list, psfpw_dict["avg_psfp7w"], "percent_selected_from_prev7_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp8w_list, psfpw_dict["avg_psfp8w"], "percent_selected_from_prev8_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp9w_list, psfpw_dict["avg_psfp9w"], "percent_selected_from_prev9_winners_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfp10w_list, psfpw_dict["avg_psfp10w"], "percent_selected_from_prev10_winners_sample_" + sample_num_str + ".txt")
    #
    #     write.write_mean_list_to_file(psfip2_list, psfip_dict["avg_psfip2"], "percent_selected_from_intersect_prev2_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip3_list, psfip_dict["avg_psfip3"], "percent_selected_from_intersect_prev3_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip4_list, psfip_dict["avg_psfip4"], "percent_selected_from_intersect_prev4_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip5_list, psfip_dict["avg_psfip5"], "percent_selected_from_intersect_prev5_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip6_list, psfip_dict["avg_psfip6"], "percent_selected_from_intersect_prev6_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip7_list, psfip_dict["avg_psfip7"], "percent_selected_from_intersect_prev7_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip8_list, psfip_dict["avg_psfip8"], "percent_selected_from_intersect_prev8_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip9_list, psfip_dict["avg_psfip9"], "percent_selected_from_intersect_prev9_losers_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(psfip10_list, psfip_dict["avg_psfip10"], "percent_selected_from_intersect_prev10_losers_sample_" + sample_num_str + ".txt")
    #
    #     write.write_mean_list_to_file(pip2ls_list, pipls_dict["avg_pip2ls"], "percent_intersect_prev2_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip3ls_list, pipls_dict["avg_pip3ls"], "percent_intersect_prev3_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip4ls_list, pipls_dict["avg_pip4ls"], "percent_intersect_prev4_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip5ls_list, pipls_dict["avg_pip5ls"], "percent_intersect_prev5_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip6ls_list, pipls_dict["avg_pip6ls"], "percent_intersect_prev6_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip7ls_list, pipls_dict["avg_pip7ls"], "percent_intersect_prev7_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip8ls_list, pipls_dict["avg_pip8ls"], "percent_intersect_prev8_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip9ls_list, pipls_dict["avg_pip9ls"], "percent_intersect_prev9_losers_selected_sample_" + sample_num_str + ".txt")
    #     write.write_mean_list_to_file(pip10ls_list, pipls_dict["avg_pip10ls"], "percent_intersect_prev10_losers_selected_sample_" + sample_num_str + ".txt")
    #
    #
    #     # write.write_mean_list_to_file(prns_list, remaining_nums_stats_dict["avg_prns"], "percent_remaining_nums_selected_sample_" + sample_num_str + ".txt")
    #     # write.write_mean_list_to_file(psfrn_list, remaining_nums_stats_dict["avg_psfrn"], "percent_selected_from_remaining_nums_sample_" + sample_num_str + ".txt")
    #     # write.write_mean_list_to_file(draws_per_round_list, remaining_nums_stats_dict["avg_draws_per_round"], "draws_per_round_sample_" + sample_num_str + ".txt")
    #
    #     # write.write_mean_list_to_file(pip2lrns_list, plirn_stats["avg_pip2lrns"], "percent_intersect_prev2_losers_remaining_nums_selected_sample_" + sample_num_str + ".txt")
    #     # write.write_mean_list_to_file(psfip2lrn_list, plirn_stats["avg_psfip2lrn"], "percent_selected_from_intersect_prev2_losers_remaining_nums_sample_" + sample_num_str + ".txt")
    #
    #
    #     # avg_draws_till_new_round = mean(draws_till_new_round_list)
    #     # write.write_mean_list_to_file(draws_till_new_round_list, avg_draws_till_new_round, "avg_draws_till_new_round_sample_" + sample_num_str + ".txt")
    #
    #     write.write_dict_to_file(avg_draw_distance_dict, "avg_draw_distances_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(spot_histogram, "spot_histogram_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(range_histogram, "range_histogram_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(mod_histogram, "mod_histogram_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(ppls_dict, "percent_prev_losers_selected_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(ppws_dict, "percent_prev_winners_selected_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(psfpl_dict, "percent_selected_from_prev_losers_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(psfpw_dict, "percent_selected_from_prev_winners_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(remaining_nums_stats_dict, "remaining_nums_set_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(plirn_stats, "previous_losers_intersect_remaining_nums_stats_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(psfip_dict, "percent_selected_from_intersect_prev_losers_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(pipls_dict, "percent_interesct_previous_losers_selected_sample_" + sample_num_str + ".json")
    #
    #     write.write_dict_to_file(draw_distance_dict, "draw_distances_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(dss.last_remaining_num_dict_list, "last_remaining_distances_sample_" + sample_num_str + ".json")
    #     write.write_dict_to_file(dss.get_draw_distance_dict_list_stats(dss.last_remaining_num_dict_list),
    #         "last_reamining_distance_sample_" + sample_num_str + ".json")
    #
    #     write.write_dict_to_file(dss.get_draw_distance_dict_list_stats(draw_distance_dict),
    #         "draw_distances_stats_sample_" + sample_num_str + ".json")
    #
    #     write.write_dict_to_file(last_n_avg_distance_dict_list, "last_n_avg_distances_sample_" + sample_num_str + ".json")
    #
    #     print("Data collection complete.")
