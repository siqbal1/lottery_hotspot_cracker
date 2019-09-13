from bs4 import BeautifulSoup
from selenium import webdriver
from HotspotResults import *
from time import sleep
from datetime import date
from statistics import mean
from sys import argv

import re
import json
import requests

from drawing_set_stats import *

num_spots_sampled = 0
num_draws_sampled = 0
current_draw_num = 0
starting_draw_num = 0

#map for historgram of numbers
spot_histogram = {}

#buckets to count winning nums
range_histogram = {
    "1-10" : 0,
    "11-20" : 0,
    "21-30" : 0,
    "31-40" : 0,
    "41-50" : 0,
    "51-60" : 0,
    "61-70" : 0,
    "71-80" : 0,
}

#historgram for # numbers in draws that are evenly divisible by dict keys
mod_histogram = {
    "odd" : 0,
    "even" : 0,
    3 : 0,
    5 : 0,
    10 : 0,
    "prime" : 0.0,
}

#list if prime numbers in range 1-80:
prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79]

#dict holds value for num of draws between when specified key was last a winning number
last_seen_dict = {}

#dict holds avg num draws between spot selections
#keep count of sum of distances
#divide by total num draws
avg_draw_distance_dict = {}

#remaining numbers set

NUM_SPOTS_PLAYED = 20
NUM_LOSING_SPOTS = 60
NUM_DRAWINGS_PER_DAY = 300


#init date to be able to get next draw numbers
INIT_DATE = date(2019, 3, 1)
INIT_DRAW_NUMBER = 2475236

def increment_draw_distance_sums(num):
    """
    Increases sum of the distance between draws in which the number
    was selected as a winner

    Input: num_spot
    """
    if not num in avg_draw_distance_dict.keys():
        last_seen_dict[num] = current_draw_num
        draw_distance = current_draw_num - starting_draw_num
        avg_draw_distance_dict[num] = draw_distance
        print("Draw Distance " + str(num) + ": " + str(draw_distance))
    else:
        #find diff in draw nums
        draw_distance = current_draw_num - last_seen_dict[num]
        avg_draw_distance_dict[num] += draw_distance
        last_seen_dict[num] = current_draw_num
        print( "Draw Distance " + str(num) + ": " + str(draw_distance))

def increment_mod_hist(num):
    """
    Increment values in mod_hist dictionary
    Input: number
    """
    if(num % 2 == 0):
        mod_histogram["even"] += 1
    else:
        mod_histogram["odd"] += 1

    if(num % 3 == 0):
        mod_histogram[3] += 1
    elif(num % 5 == 0):
        mod_histogram[5] += 1

    if(num % 10 == 0):
        mod_histogram[10] += 1

    if(num in prime_list):
        mod_histogram["prime"] += 1


def increment_range_hist(num):
    if(num >= 1 and num <= 10):
        range_histogram["1-10"] += 1
    elif(num >= 11 and num <= 20):
        range_histogram["11-20"] += 1
    elif(num >= 21 and num <= 30):
        range_histogram["21-30"] += 1
    elif(num >= 31 and num <= 40):
        range_histogram["31-40"] += 1
    elif(num >= 41 and num <= 50):
        range_histogram["41-50"] += 1
    elif(num >= 51 and num <= 60):
        range_histogram["51-60"] += 1
    elif(num >= 61 and num <= 70):
        range_histogram["61-70"] += 1
    else:
        #(num >= 71 and num <= 80):
        range_histogram["71-80"] += 1

def increment_spot_hist(num):
    if num not in spot_histogram.keys():
        spot_histogram[num] = 1
    else:
        spot_histogram[num] += 1

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

def get_stats_from_soup_list(winning_spots_soup):
    """
    Input beutiful soup list of li elements
    output: dict with
    ret_dict = {
        "spot_list" : spot_list,
        "spot_set" : spot_set,
        "mean" : mean,
    }
    """
    global num_spots_sampled

    spot_list = []
    spot_set = set()

    mean = 0

    for spot in winning_spots_soup:
        spot_int = int(spot.string)
        spot_list.append(int(spot.string))
        spot_set.add(int(spot.string))
        mean += spot_int

        #add to historgram of nums
        increment_spot_hist(spot_int)

        #add to range buckets histogram
        increment_range_hist(spot_int)


        #add to even numbers and odd numbers count
        #add to mod 5 and mod 10 count
        #add percent of primes for current draw
        increment_mod_hist(spot_int)

        #add to avg num draws between numbers selection
        increment_draw_distance_sums(spot_int)

        num_spots_sampled += 1


    mean /= float(NUM_SPOTS_PLAYED)

    ret_dict = {
        "spot_list" : spot_list,
        "spot_set" : spot_set,
        "mean" : mean,
    }

    return ret_dict


def get_most_recent_draw():
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

    print(draw_num)

    driver.quit()

    return get_stats_from_soup_list(winning_spots)


def get_results_from_draw_num(draw_num):
    """
    Uses draw number to make request to lotto page for draw number
    input: draw number
    return: dict  with
    """
    url = "https://www.calottery.com/play/draw-games/hot-spot/draw-detail?draw="
    url += str(draw_num)
    print(url)
    response = requests.get(url)

    #create BeautifulSoup object to parse winning numbers
    soup = BeautifulSoup(response.text, "html.parser")
    winning_spots = soup.find_all("li", class_=re.compile("spot win*"))

    return get_stats_from_soup_list(winning_spots)

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
    }
    """
    print("Getting past draw date...")
    year = input("Enter year: ")
    month = input("Enter month: ")
    day = input("Enter day: ")
    num_days_to_sample = input("Enter number of days to sample: ")

    if(len(year) <= 1):
        year = 2019

    if(len(month) < 1):
        print("Error: Invalid month")
        exit(0)

    if(len(day) < 1):
        print("Error: Invalid day")
        exit(0)

    ret_dict = {
        "year" : int(year),
        "month" : int(month),
        "day" : int(day),
        "num_days_to_sample" : int(num_days_to_sample)
    }

    return ret_dict

def write_mean_list_to_file(mean_list, overall_mean, f_name):
    f = open(f_name, 'w')

    f.write("Overall Mean: " + str(overall_mean) + "\n")

    for sample_mean in mean_list:
        f.write(str(sample_mean) + "\n")

    f.close()

def write_dict_to_file(any_dict, f_name):
    with open(f_name, "w") as json_file:
        json.dump(any_dict, json_file)

if __name__ == "__main__":
    #hold list of avgs of previous draws
    mean_list = []

    #hold list of percentage diff between losers/winners of prev draws and
    #current draws
    prev_result_set = set()
    prev2_result_set = set()
    prev3_result_set = set()
    prev4_result_set = set()

    curr_result_set = set()

    #percent prev losers selected -> ppls
    ppls_list = []
    pp2ls_list = []
    pp3ls_list = []
    pp4ls_list = []

    #percent prev winners selected -> ppws
    ppws_list = []
    pp2ws_list = []
    pp3ws_list = []
    pp4ws_list = []

    #percent_selected_from_prev_losers -> psfpl
    #list of percent composition of current winning numbers from previous losing numbers
    psfpl_list = []
    psfp2l_list = []
    psfp3l_list = []
    psfp4l_list = []

    #percent_selected_from_prev_winners -> psfpw
    #list of percent composition of current winning numbers from previous winning numbers
    psfpw_list = []
    psfp2w_list = []
    psfp3w_list = []
    psfp4w_list = []

    #since mean for hotspot is always around 40
    #generator will try to pick all numbers once
    #at least every 4 draws


    #list percent of winning numbers that were selected from set intersection
    #of previous draws losers
    #numbers that have lost twice in a row
    #percent intersection of previous 2 losers selected = pip2ls
    pip2ls_list = []
    pip3ls_list = []
    pip4ls_list = []

    #list of percent composition of winning numbers from intersection
    #of previous draws losers
    #percent selected from intersection of previous 2 losers -> psfip2
    psfip2_list = []
    psfip3_list = []
    psfip4_list = []

    #list of percent of remaining_nums_set selected for current draws
    #percent remaining nums selected -> prns
    prns_list = []

    #list of percent composition of current draw set from remaining_nums_set
    #percent selected from remaining_nums_set -> psfrn
    psfrn_list = []

    #list for num draws needed before 1 round is complete
    #one round is the num of draws needed for all nums in range
    #1-80 to be selected as winners
    draws_per_round_list = []

    #list for percentage of intersection of prev2 losers and remaining_nums_set selected in current draw
    #percent intersect prev2 losers remaining nums selected ->pip2lrns
    pip2lrns_list = []

    #list for percent composition of current draw from intersection of prev2 losers and remaining_nums_set
    #percent selected from intersect prev2 losers remaining nums -> psfip2lrn
    psfip2lrn_list = []

    start_date = 0

    #get continuous results
    try:
        #mode 0 : get current draws
        #mode 1 : get past draw numbers
        if(len(argv) == 2):
            #get date
            prompt_dict = prompt_for_date()
            print(prompt_dict)

            start_date = date(prompt_dict["year"], prompt_dict["month"], prompt_dict["day"])
            print(start_date)

            starting_draw_num = date_to_draw_number(start_date)
            current_draw_num = starting_draw_num
            print(current_draw_num)

            total_num_draws_to_sample = prompt_dict["num_days_to_sample"] * NUM_DRAWINGS_PER_DAY
            num_draws_sampled = 0

            while(num_draws_sampled < total_num_draws_to_sample):
                print(num_draws_sampled, current_draw_num)

                result_dict = get_results_from_draw_num(current_draw_num)
                print_dict(result_dict)

                mean_list.append(result_dict["mean"])

                #conditions for first 4 draws
                if(num_draws_sampled <= 3):
                    if(num_draws_sampled == 0):
                        curr_result_set = result_dict["spot_set"]
                    elif(num_draws_sampled == 1):
                        prev_result_set = curr_result_set
                        curr_result_set = result_dict["spot_set"]
                    elif(num_draws_sampled == 2):
                        prev2_result_set = prev_result_set
                        prev_result_set = curr_result_set
                        curr_result_set = result_dict["spot_set"]
                    elif(num_draws_sampled == 3):
                        prev3_result_set = prev2_result_set
                        prev2_result_set = prev_result_set
                        prev_result_set = curr_result_set
                        curr_result_set = result_dict["spot_set"]
                else:
                    #we have atleast 4 results sets to work with
                    #get set statistics
                    prev4_result_set = prev3_result_set
                    prev3_result_set = prev2_result_set
                    prev2_result_set = prev_result_set
                    prev_result_set = curr_result_set
                    curr_result_set = result_dict["spot_set"]

                    set_stats_dict = get_set_stats(curr_result_set, prev_result_set, prev2_result_set,
                        prev3_result_set, prev4_result_set)

                    #parse results and append to lists
                    parse_ppls_set_stats(set_stats_dict, ppls_list, pp2ls_list, pp3ls_list, pp4ls_list)
                    parse_ppws_set_stats(set_stats_dict, ppws_list, pp2ws_list, pp3ws_list, pp4ws_list)
                    parse_psfpl_set_stats(set_stats_dict, psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list)
                    parse_psfpw_set_stats(set_stats_dict, psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list)
                    parse_pipls_set_stats(set_stats_dict, pip2ls_list, pip3ls_list, pip4ls_list)
                    parse_psfip_set_stats(set_stats_dict, psfip2_list, psfip3_list, psfip4_list)
                    parse_remaining_nums_set_stats(set_stats_dict, prns_list, psfrn_list, draws_per_round_list)
                    parse_intersect_remaining_num_set_stats(set_stats_dict, pip2lrns_list, psfip2lrn_list)

                num_draws_sampled += 1
                current_draw_num += 1



        else:
            #get current draw stats
            while(1):
                result_dict = get_most_recent_draw()

                if len(current_result_set) == 0:
                    curr_result_set = result_dict["spot_set"]


            print("Waiting for next draw...")
            wait_n_minutes(4)

    except Exception as e:
        print(e)

    finally:
        #print final stats
        #save to all lists to files
        print("Last draw num: " + str(current_draw_num))
        #print("Starting from " + str(start_date) + " attempted to get results for " + total_num_draws_to_sample + " draws")
        print("Num spots sampled: " + str(num_spots_sampled))
        print("Num draws sampled: " + str(num_draws_sampled))

        #get avg draw distance
        #avg_draw_distance_dict holds sums of distances
        for key in avg_draw_distance_dict.keys():
            # get avg by dividing the sum of draw distances / num times a num is played
            avg_draw_distance_dict[key] /= float(spot_histogram[key])

        #avg draw distance for all numbers
        avg_draw_distance_dict["avg_over_all"] = mean(avg_draw_distance_dict.values())

        #print all historgrams
        print_dict(spot_histogram)
        print_dict(range_histogram)
        print_dict(mod_histogram)


        #print all set stats
        #get avg for al percent changes between losers and winners of previous sets
        ppls_dict = get_ppls_stats(ppls_list, pp2ls_list, pp3ls_list, pp4ls_list)
        ppws_dict = get_ppws_stats(ppws_list, pp2ws_list, pp3ws_list, pp4ws_list)
        psfpl_dict = get_psfpl_stats(psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list)
        psfpw_dict = get_psfpw_stats(psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list)
        remaining_nums_stats_dict = get_remaining_nums_stats(prns_list, psfrn_list, draws_per_round_list)

        #prev losers intersect remaining nums stats -> plirn_stats
        plirn_stats = get_plirn_stats(pip2lrns_list, psfip2lrn_list)

        #write everything to files
        overall_mean = mean(mean_list)
        write_mean_list_to_file(mean_list, overall_mean, "sample_means_list.txt")

        write_mean_list_to_file(ppls_list, ppls_dict["avg_ppls"], "percent_previous_losers_selected_list.txt")
        write_mean_list_to_file(pp2ls_list, ppls_dict["avg_pp2ls"], "percent_previous_2_losers_selected_list.txt")
        write_mean_list_to_file(pp3ls_list, ppls_dict["avg_pp3ls"], "percent_previous_3_losers_selected_list.txt")
        write_mean_list_to_file(pp4ls_list, ppls_dict["avg_pp4ls"], "percent_previous_4_losers_selected_list.txt")

        write_mean_list_to_file(ppws_list, ppws_dict["avg_ppws"], "percent_previous_winners_selected_list.txt")
        write_mean_list_to_file(pp2ws_list, ppws_dict["avg_pp2ws"], "percent_previous_2_winners_selected_list.txt")
        write_mean_list_to_file(pp3ws_list, ppws_dict["avg_pp3ws"], "percent_previous_3_winners_selected_list.txt")
        write_mean_list_to_file(pp4ws_list, ppws_dict["avg_pp4ws"], "percent_previous_4_winners_selected_list.txt")

        write_mean_list_to_file(psfpl_list, psfpl_dict["avg_psfpl"], "percent_selected_from_prev_losers.txt")
        write_mean_list_to_file(psfp2l_list, psfpl_dict["avg_psfp2l"], "percent_selected_from_prev2_losers.txt")
        write_mean_list_to_file(psfp3l_list, psfpl_dict["avg_psfp3l"], "percent_selected_from_prev3_losers.txt")
        write_mean_list_to_file(psfp4l_list, psfpl_dict["avg_psfp4l"], "percent_selected_from_prev4_losers.txt")

        write_mean_list_to_file(psfpw_list, psfpw_dict["avg_psfpw"], "percent_selected_from_prev_winners.txt")
        write_mean_list_to_file(psfp2w_list, psfpw_dict["avg_psfp2w"], "percent_selected_from_prev2_winners.txt")
        write_mean_list_to_file(psfp3w_list, psfpw_dict["avg_psfp3w"], "percent_selected_from_prev3_winners.txt")
        write_mean_list_to_file(psfp4w_list, psfpw_dict["avg_psfp4w"], "percent_selected_from_prev4_winners.txt")


        write_mean_list_to_file(prns_list, remaining_nums_stats_dict["avg_prns"], "percent_remaining_nums_selected.txt")
        write_mean_list_to_file(psfrn_list, remaining_nums_stats_dict["avg_psfrn"], "percent_selected_from_remaining_nums.txt")
        write_mean_list_to_file(draws_per_round_list, remaining_nums_stats_dict["avg_draws_per_round"], "draws_per_round.txt")

        write_mean_list_to_file(pip2lrns_list, plirn_stats["avg_pip2lrns"], "percent_intersect_prev2_losers_remaining_nums_selected")
        write_mean_list_to_file(psfip2lrn_list, plirn_stats["avg_psfip2lrn"], "percent_selected_from_intersect_prev2_losers_remaining_nums")

        write_dict_to_file(avg_draw_distance_dict, "avg_draw_distances.json")
        write_dict_to_file(spot_histogram, "spot_histogram.json")
        write_dict_to_file(range_histogram, "range_histogram.json")
        write_dict_to_file(mod_histogram, "mod_histogram.json")
        write_dict_to_file(ppls_dict, "percent_prev_losers_selected_stats.json")
        write_dict_to_file(ppws_dict, "percent_prev_winners_selected_stats.json")
        write_dict_to_file(psfpl_dict, "percent_selected_from_prev_losers_stats.json")
        write_dict_to_file(psfpw_dict, "percent_selected_from_prev_winners_stats.json")
        write_dict_to_file(remaining_nums_stats_dict, "remaining_nums_set_stats.json")
        write_dict_to_file(plirn_stats, "previous_losers_intersect_remaining_nums_stats.json")

        print("Data collection complete.")
