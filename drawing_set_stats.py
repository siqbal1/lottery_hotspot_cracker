from statistics import mean
from statistics import stdev
from statistics import variance
import past_draws_stats as pds


#set for all numbers in hotspot range
range_set = set()
#set to keep track of the numbers that have not been played
#in current round
#when all numbers have been played
#increment count and reset the remaining_nums_set
#find avg num draws that it takes to use all nums at least once
#find percentage of current draw that comes from
#the numbers that havent been played during this round
remaining_nums_set = set()

for i in range(1, 81):
    range_set.add(i)
    remaining_nums_set.add(i)

#keep track of amount of draws needed to complete one round
#one round is complete when the remaining_nums_set becomes empty
#and is reset
num_draws_in_round = 0

#keep track of the last 10 remaining nums in set
#how many draws after it was the last remaining num is it selected again

#key: spot_num value: draw number when it was the last 10 elements
last_remaining_num = 0
last_remaining_num_dict = dict()
#last_remaining_num_dict_list = init_spot_dict_list()

draws_till_new_round = 0

#list of lists of a avgs of the inter-drawing count of last i elements in



def reset_remaining_nums_set():
    return init_range_set()

def update_remaining_nums_set(remaining_nums_set, current_draw_set, num_draws_in_round, last_remaining_num=None, last_remaining_num_dict=None,
    current_draw_num=None):
    """
    input: current draw set
    return: dict {
        new remaining_nums_set,
        round number if new round started (0 otherwise)
    }
    """
    ret_dict = dict()



    ret_set = remaining_nums_set - current_draw_set
    updated_draws_in_round = num_draws_in_round
    # print(remaining_nums_set)

    print("Ret set:", ret_set)

    #if not eneough data points
    #reset anyways to not skew stats
    if(len(ret_set) < 6):

        if(last_remaining_num_dict is not None):
            #if only one item in set save it
            #get current draw number
            for num in remaining_nums_set:
                # print("Remaining_set_almost empty, current draw #:", current_draw_num, "\n\n")
                last_remaining_num_dict[num] = current_draw_num



        ret_set = reset_remaining_nums_set()
        temp = num_draws_in_round
        updated_draws_in_round = 0



    else:
        updated_draws_in_round += 1

    ret_dict["remaining_nums_set"] = ret_set
    ret_dict["num_draws_in_round"] = updated_draws_in_round

    return ret_dict




def print_dict(any_dict):
    for key, value in any_dict.items():
        print(key, value)

def get_set_stats(current_draw_num, current_draw_set, prev_draw_set, prev2_draw_set,
    prev3_draw_set, prev4_draw_set, prev5_draw_set, prev6_draw_set,
    prev7_draw_set, prev8_draw_set, prev9_draw_set, prev10_draw_set):
    """
    Input: current and last 10 sets
    Output: dict with set statistics

    ret_dict {
        percent_prev_losers_selected
        percent_prev2_losers_selected
        percent_prev3_losers_selected
        percent_prev4_losers_selected

        percent_prev_winners_selected
        percent_prev2_winners_selected
        percent_prev3_winners_selected
        percent_prev4_winners_selected
    }
    """
    global remaining_nums_set
    global last_remaining_num
    global draws_till_new_round

    set_stats_dict = {}

    #set of nums for all losers for the draws
    prev_losers_selected = get_losers_for_draw_set(prev_draw_set)
    prev2_losers_selected = get_losers_for_draw_set(prev2_draw_set)
    prev3_losers_selected = get_losers_for_draw_set(prev3_draw_set)
    prev4_losers_selected = get_losers_for_draw_set(prev4_draw_set)
    prev5_losers_selected = get_losers_for_draw_set(prev5_draw_set)
    prev6_losers_selected = get_losers_for_draw_set(prev6_draw_set)
    prev7_losers_selected = get_losers_for_draw_set(prev7_draw_set)
    prev8_losers_selected = get_losers_for_draw_set(prev8_draw_set)
    prev9_losers_selected = get_losers_for_draw_set(prev9_draw_set)
    prev10_losers_selected = get_losers_for_draw_set(prev10_draw_set)


    print("Prev Losers: ")
    print(prev_losers_selected)
    # print("Prev 2 Losers: ")
    # print(prev2_losers_selected)
    # print("Prev 3 Losers: ")
    # print(prev3_losers_selected)
    # print("Prev 4 Losers: ")
    # print(prev4_losers_selected)
    # print("Prev 5 Losers: ")
    # print(prev5_losers_selected)
    # print("Prev 6 Losers: ")
    # print(prev6_losers_selected)
    # print("Prev 7 Losers: ")
    # print(prev7_losers_selected)
    # print("Prev 8 Losers: ")
    # print(prev8_losers_selected)
    # print("Prev 9 Losers: ")
    # print(prev9_losers_selected)
    # print("Prev 10 Losers: ")
    # print(prev10_losers_selected)


    #set of numbers for intersection of losers
    #get the percentage of common losing numbers across multiple draws
    #compare with current draw to get a percentage
    intersect_prev2_losers = prev_losers_selected.intersection(prev2_losers_selected)
    intersect_prev3_losers = intersect_prev2_losers.intersection(prev3_losers_selected)
    intersect_prev4_losers = intersect_prev3_losers.intersection(prev4_losers_selected)
    intersect_prev5_losers = intersect_prev4_losers.intersection(prev5_losers_selected)
    intersect_prev6_losers = intersect_prev5_losers.intersection(prev6_losers_selected)
    intersect_prev7_losers = intersect_prev6_losers.intersection(prev7_losers_selected)
    intersect_prev8_losers = intersect_prev7_losers.intersection(prev8_losers_selected)
    intersect_prev9_losers = intersect_prev8_losers.intersection(prev9_losers_selected)
    intersect_prev10_losers = intersect_prev9_losers.intersection(prev10_losers_selected)


    #highest percent of nums come from prev2 losers and remaining nums
    #find percentage of the intersect that appear
    intersect_prev2_losers_remaining_nums = intersect_prev2_losers.intersection(remaining_nums_set)

    print("Intersect Prev 2 losers")
    print(intersect_prev2_losers)
    print("Intersect Prev 3 losers")
    print(intersect_prev3_losers)
    print("Intersect Prev 4 losers")
    print(intersect_prev4_losers)
    print("Intersect Prev 5 losers")
    print(intersect_prev5_losers)
    print("Intersect Prev 6 losers")
    print(intersect_prev6_losers)
    print("Intersect Prev 7 losers")
    print(intersect_prev7_losers)
    print("Intersect Prev 8 losers")
    print(intersect_prev8_losers)
    print("Intersect Prev 9 losers")
    print(intersect_prev9_losers)
    print("Intersect Prev 10 losers")
    print(intersect_prev10_losers)



    # print("Intersect Prev 2 losers and remaining nums")
    # print(intersect_prev2_losers_remaining_nums)

    #percent common between losers of prev sets and winner of current set
    set_stats_dict["percent_prev_losers_selected"] = get_percent_common_s2(current_draw_set, prev_losers_selected)
    set_stats_dict["percent_prev2_losers_selected"] = get_percent_common_s2(current_draw_set, prev2_losers_selected)
    set_stats_dict["percent_prev3_losers_selected"] = get_percent_common_s2(current_draw_set, prev3_losers_selected)
    set_stats_dict["percent_prev4_losers_selected"] = get_percent_common_s2(current_draw_set, prev4_losers_selected)
    set_stats_dict["percent_prev5_losers_selected"] = get_percent_common_s2(current_draw_set, prev5_losers_selected)
    set_stats_dict["percent_prev6_losers_selected"] = get_percent_common_s2(current_draw_set, prev6_losers_selected)
    set_stats_dict["percent_prev7_losers_selected"] = get_percent_common_s2(current_draw_set, prev7_losers_selected)
    set_stats_dict["percent_prev8_losers_selected"] = get_percent_common_s2(current_draw_set, prev8_losers_selected)
    set_stats_dict["percent_prev9_losers_selected"] = get_percent_common_s2(current_draw_set, prev9_losers_selected)
    set_stats_dict["percent_prev10_losers_selected"] = get_percent_common_s2(current_draw_set, prev10_losers_selected)


    #percent of how much of the winning numbers came from previous loser sets
    #percent composition of prev losers to curr winners
    set_stats_dict["percent_selected_from_prev_losers"] = get_percent_common_s1(current_draw_set, prev_losers_selected)
    set_stats_dict["percent_selected_from_prev2_losers"] = get_percent_common_s1(current_draw_set, prev2_losers_selected)
    set_stats_dict["percent_selected_from_prev3_losers"] = get_percent_common_s1(current_draw_set, prev3_losers_selected)
    set_stats_dict["percent_selected_from_prev4_losers"] = get_percent_common_s1(current_draw_set, prev4_losers_selected)
    set_stats_dict["percent_selected_from_prev5_losers"] = get_percent_common_s1(current_draw_set, prev5_losers_selected)
    set_stats_dict["percent_selected_from_prev6_losers"] = get_percent_common_s1(current_draw_set, prev6_losers_selected)
    set_stats_dict["percent_selected_from_prev7_losers"] = get_percent_common_s1(current_draw_set, prev7_losers_selected)
    set_stats_dict["percent_selected_from_prev8_losers"] = get_percent_common_s1(current_draw_set, prev8_losers_selected)
    set_stats_dict["percent_selected_from_prev9_losers"] = get_percent_common_s1(current_draw_set, prev9_losers_selected)
    set_stats_dict["percent_selected_from_prev10_losers"] = get_percent_common_s1(current_draw_set, prev10_losers_selected)

    #percent common between winners of prev sets and winners of current set
    set_stats_dict["percent_prev_winners_selected"] = get_percent_common_s2(current_draw_set, prev_draw_set)
    set_stats_dict["percent_prev2_winners_selected"] = get_percent_common_s2(current_draw_set, prev2_draw_set)
    set_stats_dict["percent_prev3_winners_selected"] = get_percent_common_s2(current_draw_set, prev3_draw_set)
    set_stats_dict["percent_prev4_winners_selected"] = get_percent_common_s2(current_draw_set, prev4_draw_set)
    set_stats_dict["percent_prev5_winners_selected"] = get_percent_common_s2(current_draw_set, prev5_draw_set)
    set_stats_dict["percent_prev6_winners_selected"] = get_percent_common_s2(current_draw_set, prev6_draw_set)
    set_stats_dict["percent_prev7_winners_selected"] = get_percent_common_s2(current_draw_set, prev7_draw_set)
    set_stats_dict["percent_prev8_winners_selected"] = get_percent_common_s2(current_draw_set, prev8_draw_set)
    set_stats_dict["percent_prev9_winners_selected"] = get_percent_common_s2(current_draw_set, prev9_draw_set)
    set_stats_dict["percent_prev10_winners_selected"] = get_percent_common_s2(current_draw_set, prev10_draw_set)

    #percent of how much of the winning numbers came from previous winning sets
    #percent composition of prev winners to curr winners
    set_stats_dict["percent_selected_from_prev_winners"] = get_percent_common_s1(current_draw_set, prev_draw_set)
    set_stats_dict["percent_selected_from_prev2_winners"] = get_percent_common_s1(current_draw_set, prev2_draw_set)
    set_stats_dict["percent_selected_from_prev3_winners"] = get_percent_common_s1(current_draw_set, prev3_draw_set)
    set_stats_dict["percent_selected_from_prev4_winners"] = get_percent_common_s1(current_draw_set, prev4_draw_set)
    set_stats_dict["percent_selected_from_prev5_winners"] = get_percent_common_s1(current_draw_set, prev5_draw_set)
    set_stats_dict["percent_selected_from_prev6_winners"] = get_percent_common_s1(current_draw_set, prev6_draw_set)
    set_stats_dict["percent_selected_from_prev7_winners"] = get_percent_common_s1(current_draw_set, prev7_draw_set)
    set_stats_dict["percent_selected_from_prev8_winners"] = get_percent_common_s1(current_draw_set, prev8_draw_set)
    set_stats_dict["percent_selected_from_prev9_winners"] = get_percent_common_s1(current_draw_set, prev9_draw_set)
    set_stats_dict["percent_selected_from_prev10_winners"] = get_percent_common_s1(current_draw_set, prev10_draw_set)

    #percent of how many of the previous common losers (among previous draws) were
    #selected as winners in the current draw
    set_stats_dict["percent_intersect_prev2_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev2_losers)
    set_stats_dict["percent_intersect_prev3_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev3_losers)
    set_stats_dict["percent_intersect_prev4_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev4_losers)
    set_stats_dict["percent_intersect_prev5_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev5_losers)
    set_stats_dict["percent_intersect_prev6_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev6_losers)
    set_stats_dict["percent_intersect_prev7_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev7_losers)
    set_stats_dict["percent_intersect_prev8_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev8_losers)
    set_stats_dict["percent_intersect_prev9_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev9_losers)
    set_stats_dict["percent_intersect_prev10_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev10_losers)

    #percent composition of the current draw winning numbers from intersection of prev draw losers
    set_stats_dict["percent_selected_from_intersect_prev2_losers"] = get_percent_common_s1(current_draw_set, intersect_prev2_losers)
    set_stats_dict["percent_selected_from_intersect_prev3_losers"] = get_percent_common_s1(current_draw_set, intersect_prev3_losers)
    set_stats_dict["percent_selected_from_intersect_prev4_losers"] = get_percent_common_s1(current_draw_set, intersect_prev4_losers)
    set_stats_dict["percent_selected_from_intersect_prev5_losers"] = get_percent_common_s1(current_draw_set, intersect_prev5_losers)
    set_stats_dict["percent_selected_from_intersect_prev6_losers"] = get_percent_common_s1(current_draw_set, intersect_prev6_losers)
    set_stats_dict["percent_selected_from_intersect_prev7_losers"] = get_percent_common_s1(current_draw_set, intersect_prev7_losers)
    set_stats_dict["percent_selected_from_intersect_prev8_losers"] = get_percent_common_s1(current_draw_set, intersect_prev8_losers)
    set_stats_dict["percent_selected_from_intersect_prev9_losers"] = get_percent_common_s1(current_draw_set, intersect_prev9_losers)
    set_stats_dict["percent_selected_from_intersect_prev10_losers"] = get_percent_common_s1(current_draw_set, intersect_prev10_losers)

    #get percent of remaining nums selected as winners in current draw
    set_stats_dict["percent_remaining_nums_selected"] = get_percent_common_s2(current_draw_set, remaining_nums_set)
    #percent composition of current winning nums from the remaining losing nums set
    set_stats_dict["percent_selected_from_remaining_nums"] = get_percent_common_s1(current_draw_set, remaining_nums_set)

    #percent of the intersect of the prev2 losers and remaining nums that are selected as winners
    set_stats_dict["percent_intersect_prev2_losers_remaining_nums_selected"] = get_percent_common_s2(current_draw_set, intersect_prev2_losers_remaining_nums)
    #percent composition of current winning numbers with the intersect of prev 2 losers and remaining nums
    set_stats_dict["percent_selected_from_intersect_prev2_losers_remaining_nums"] = get_percent_common_s1(current_draw_set, intersect_prev2_losers_remaining_nums)

    #update remaining nums set to get rid of most recent winning nums
    #if remaining_nums_set empty return num draws that it took
    # round_len = update_remaining_nums_set(current_draw_set, current_draw_num)
    # if(round_len > 0):
    #     set_stats_dict["num_draws_in_round"] = round_len
    #
    # if(last_remaining_num > 0):
    #     if(last_remaining_num in current_draw_set):
    #         set_stats_dict["draws_till_new_round"] = draws_till_new_round
    #         #rst and wait till next round is about to complete
    #         last_remaining_num = 0
    #         draws_till_new_round = 0
    #     else:
    #         draws_till_new_round += 1
    #


    print_dict(set_stats_dict)
    return set_stats_dict


def get_losers_for_draw_set(draw_set):
    """
    Input: draw_set
    output: set of losing numbers for that draw
    """
    return range_set - draw_set

def get_percent_common_s1(s1, s2):
    """
    Input: set1, set2
    output: percent of composition of s1 from s2
    """
    #s2 = prev_set
    #s1 = curr_set
    common_set = s1.intersection(s2)

    #percent composition of s1 from s2
    if len(s1) > 0:
        return len(common_set) / float(len(s1))
    else:
        return "N/A"


def get_percent_common_s2(s1, s2):
    """
    Input: set1, set2
    output: percent of nums in current_set that exists in the other set s2
    """

    #s2 = prev_set
    #s1 = curr_set
    common_set = s1.intersection(s2)

    #percent of s1 that comes from s2
    if len(s2) > 0:
        return len(common_set) / float(len(s2))
    else:
        return "N/A"


def parse_ppls_set_stats(set_stats_dict, ppls_list, pp2ls_list, pp3ls_list, pp4ls_list,
    pp5ls_list, pp6ls_list, pp7ls_list, pp8ls_list, pp9ls_list, pp10ls_list):
    #percent previous losers selected
    ppls_list.append(set_stats_dict["percent_prev_losers_selected"])
    pp2ls_list.append(set_stats_dict["percent_prev2_losers_selected"])
    pp3ls_list.append(set_stats_dict["percent_prev3_losers_selected"])
    pp4ls_list.append(set_stats_dict["percent_prev4_losers_selected"])
    pp5ls_list.append(set_stats_dict["percent_prev5_losers_selected"])
    pp6ls_list.append(set_stats_dict["percent_prev6_losers_selected"])
    pp7ls_list.append(set_stats_dict["percent_prev7_losers_selected"])
    pp8ls_list.append(set_stats_dict["percent_prev8_losers_selected"])
    pp9ls_list.append(set_stats_dict["percent_prev9_losers_selected"])
    pp10ls_list.append(set_stats_dict["percent_prev10_losers_selected"])

def parse_ppws_set_stats(set_stats_dict, ppws_list, pp2ws_list, pp3ws_list, pp4ws_list,
    pp5ws_list, pp6ws_list, pp7ws_list, pp8ws_list, pp9ws_list, pp10ws_list):
    #percent previous winners selected
    ppws_list.append(set_stats_dict["percent_prev_winners_selected"])
    pp2ws_list.append(set_stats_dict["percent_prev2_winners_selected"])
    pp3ws_list.append(set_stats_dict["percent_prev3_winners_selected"])
    pp4ws_list.append(set_stats_dict["percent_prev4_winners_selected"])
    pp5ws_list.append(set_stats_dict["percent_prev5_winners_selected"])
    pp6ws_list.append(set_stats_dict["percent_prev6_winners_selected"])
    pp7ws_list.append(set_stats_dict["percent_prev7_winners_selected"])
    pp8ws_list.append(set_stats_dict["percent_prev8_winners_selected"])
    pp9ws_list.append(set_stats_dict["percent_prev9_winners_selected"])
    pp10ws_list.append(set_stats_dict["percent_prev10_winners_selected"])

def parse_psfpl_set_stats(set_stats_dict, psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list,
    psfp5l_list, psfp6l_list, psfp7l_list, psfp8l_list, psfp9l_list, psfp10l_list):
    #percent selected from previous losers
    psfpl_list.append(set_stats_dict["percent_selected_from_prev_losers"])
    psfp2l_list.append(set_stats_dict["percent_selected_from_prev2_losers"])
    psfp3l_list.append(set_stats_dict["percent_selected_from_prev3_losers"])
    psfp4l_list.append(set_stats_dict["percent_selected_from_prev4_losers"])
    psfp5l_list.append(set_stats_dict["percent_selected_from_prev5_losers"])
    psfp6l_list.append(set_stats_dict["percent_selected_from_prev6_losers"])
    psfp7l_list.append(set_stats_dict["percent_selected_from_prev7_losers"])
    psfp8l_list.append(set_stats_dict["percent_selected_from_prev8_losers"])
    psfp9l_list.append(set_stats_dict["percent_selected_from_prev9_losers"])
    psfp10l_list.append(set_stats_dict["percent_selected_from_prev10_losers"])

def parse_psfpw_set_stats(set_stats_dict, psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list,
    psfp5w_list, psfp6w_list, psfp7w_list, psfp8w_list, psfp9w_list, psfp10w_list):
    #percent selected from previous winners
    psfpw_list.append(set_stats_dict["percent_selected_from_prev_winners"])
    psfp2w_list.append(set_stats_dict["percent_selected_from_prev2_winners"])
    psfp3w_list.append(set_stats_dict["percent_selected_from_prev3_winners"])
    psfp4w_list.append(set_stats_dict["percent_selected_from_prev4_winners"])
    psfp5w_list.append(set_stats_dict["percent_selected_from_prev5_winners"])
    psfp6w_list.append(set_stats_dict["percent_selected_from_prev6_winners"])
    psfp7w_list.append(set_stats_dict["percent_selected_from_prev7_winners"])
    psfp8w_list.append(set_stats_dict["percent_selected_from_prev8_winners"])
    psfp9w_list.append(set_stats_dict["percent_selected_from_prev9_winners"])
    psfp10w_list.append(set_stats_dict["percent_selected_from_prev10_winners"])

def parse_pipls_set_stats(set_stats_dict, pip2ls_list, pip3ls_list, pip4ls_list,
    pip5ls_list, pip6ls_list, pip7ls_list, pip8ls_list, pip9ls_list, pip10ls_list):
    #percent intersect previous losers selected

    if(set_stats_dict["percent_intersect_prev2_losers_selected"] != "N/A"):
        pip2ls_list.append(set_stats_dict["percent_intersect_prev2_losers_selected"])

    if(set_stats_dict["percent_intersect_prev3_losers_selected"] != "N/A"):
        pip3ls_list.append(set_stats_dict["percent_intersect_prev3_losers_selected"])

    if(set_stats_dict["percent_intersect_prev4_losers_selected"] != "N/A"):
        pip4ls_list.append(set_stats_dict["percent_intersect_prev4_losers_selected"])

    if(set_stats_dict["percent_intersect_prev5_losers_selected"] != "N/A"):
        pip5ls_list.append(set_stats_dict["percent_intersect_prev5_losers_selected"])

    if(set_stats_dict["percent_intersect_prev6_losers_selected"] != "N/A"):
        pip6ls_list.append(set_stats_dict["percent_intersect_prev6_losers_selected"])

    if(set_stats_dict["percent_intersect_prev7_losers_selected"] != "N/A"):
        pip7ls_list.append(set_stats_dict["percent_intersect_prev7_losers_selected"])

    if(set_stats_dict["percent_intersect_prev8_losers_selected"] != "N/A"):
        pip8ls_list.append(set_stats_dict["percent_intersect_prev8_losers_selected"])

    if(set_stats_dict["percent_intersect_prev9_losers_selected"] != "N/A"):
        pip9ls_list.append(set_stats_dict["percent_intersect_prev9_losers_selected"])

    if(set_stats_dict["percent_intersect_prev10_losers_selected"] != "N/A"):
        pip10ls_list.append(set_stats_dict["percent_intersect_prev10_losers_selected"])


def parse_psfip_set_stats(set_stats_dict, psfip2_list, psfip3_list, psfip4_list,
    psfip5_list, psfip6_list, psfip7_list, psfip8_list, psfip9_list, psfip10_list):
    #psfip -> percent_selected_from_intersect_prev_losers
    if(set_stats_dict["percent_selected_from_intersect_prev2_losers"] != "N/A"):
        psfip2_list.append(set_stats_dict["percent_selected_from_intersect_prev2_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev3_losers"] != "N/A"):
        psfip3_list.append(set_stats_dict["percent_selected_from_intersect_prev3_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev4_losers"] != "N/A"):
        psfip4_list.append(set_stats_dict["percent_selected_from_intersect_prev4_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev5_losers"] != "N/A"):
        psfip5_list.append(set_stats_dict["percent_selected_from_intersect_prev5_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev6_losers"] != "N/A"):
        psfip6_list.append(set_stats_dict["percent_selected_from_intersect_prev6_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev7_losers"] != "N/A"):
        psfip7_list.append(set_stats_dict["percent_selected_from_intersect_prev7_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev8_losers"] != "N/A"):
        psfip8_list.append(set_stats_dict["percent_selected_from_intersect_prev8_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev9_losers"] != "N/A"):
        psfip9_list.append(set_stats_dict["percent_selected_from_intersect_prev9_losers"])

    if(set_stats_dict["percent_selected_from_intersect_prev10_losers"] != "N/A"):
        psfip10_list.append(set_stats_dict["percent_selected_from_intersect_prev10_losers"])

def parse_remaining_nums_set_stats(set_stats_dict, prns_list, psfrn_list, draws_per_round_list):
    prns_list.append(set_stats_dict["percent_remaining_nums_selected"])
    psfrn_list.append(set_stats_dict["percent_selected_from_remaining_nums"])

    if("num_draws_in_round" in set_stats_dict.keys()):
        draws_per_round_list.append(set_stats_dict["num_draws_in_round"])

def parse_intersect_remaining_num_set_stats(set_stats_dict, pip2lrns_list, psfip2lrn_list):
    pip2lrns_list.append(set_stats_dict["percent_intersect_prev2_losers_remaining_nums_selected"])
    psfip2lrn_list.append(set_stats_dict["percent_selected_from_intersect_prev2_losers_remaining_nums"])

def get_ppls_stats(ppls_list, pp2ls_list, pp3ls_list, pp4ls_list, pp5ls_list,
    pp6ls_list, pp7ls_list, pp8ls_list, pp9ls_list, pp10ls_list):
    """
    ppls -> percent previous losers selected
    """
    result_dict = {}

    result_dict["avg_ppls"] = mean(ppls_list)
    result_dict["avg_pp2ls"] = mean(pp2ls_list)
    result_dict["avg_pp3ls"] = mean(pp3ls_list)
    result_dict["avg_pp4ls"] = mean(pp4ls_list)
    result_dict["avg_pp5ls"] = mean(pp5ls_list)
    result_dict["avg_pp6ls"] = mean(pp6ls_list)
    result_dict["avg_pp7ls"] = mean(pp7ls_list)
    result_dict["avg_pp8ls"] = mean(pp8ls_list)
    result_dict["avg_pp9ls"] = mean(pp9ls_list)
    result_dict["avg_pp10ls"] = mean(pp10ls_list)

    result_dict["std_dev_ppls"] = stdev(ppls_list, xbar=result_dict["avg_ppls"])
    result_dict["std_dev_pp2ls"] = stdev(pp2ls_list, xbar=result_dict["avg_pp2ls"])
    result_dict["std_dev_pp3ls"] = stdev(pp3ls_list, xbar=result_dict["avg_pp3ls"])
    result_dict["std_dev_pp4ls"] = stdev(pp4ls_list, xbar=result_dict["avg_pp4ls"])
    result_dict["std_dev_pp5ls"] = stdev(pp5ls_list, xbar=result_dict["avg_pp5ls"])
    result_dict["std_dev_pp6ls"] = stdev(pp6ls_list, xbar=result_dict["avg_pp6ls"])
    result_dict["std_dev_pp7ls"] = stdev(pp7ls_list, xbar=result_dict["avg_pp7ls"])
    result_dict["std_dev_pp8ls"] = stdev(pp8ls_list, xbar=result_dict["avg_pp8ls"])
    result_dict["std_dev_pp9ls"] = stdev(pp9ls_list, xbar=result_dict["avg_pp9ls"])
    result_dict["std_dev_pp10ls"] = stdev(pp10ls_list, xbar=result_dict["avg_pp10ls"])

    result_dict["variance_ppls"] = variance(ppls_list, xbar=result_dict["avg_ppls"])
    result_dict["variance_pp2ls"] = variance(pp2ls_list, xbar=result_dict["avg_pp2ls"])
    result_dict["variance_pp3ls"] = variance(pp3ls_list, xbar=result_dict["avg_pp3ls"])
    result_dict["variance_pp4ls"] = variance(pp4ls_list, xbar=result_dict["avg_pp4ls"])
    result_dict["variance_pp5ls"] = variance(pp5ls_list, xbar=result_dict["avg_pp5ls"])
    result_dict["variance_pp6ls"] = variance(pp6ls_list, xbar=result_dict["avg_pp6ls"])
    result_dict["variance_pp7ls"] = variance(pp7ls_list, xbar=result_dict["avg_pp7ls"])
    result_dict["variance_pp8ls"] = variance(pp8ls_list, xbar=result_dict["avg_pp8ls"])
    result_dict["variance_pp9ls"] = variance(pp9ls_list, xbar=result_dict["avg_pp9ls"])
    result_dict["variance_pp10ls"] = variance(pp10ls_list, xbar=result_dict["avg_pp10ls"])

    return result_dict

def get_ppws_stats(ppws_list, pp2ws_list, pp3ws_list, pp4ws_list, pp5ws_list,
    pp6ws_list, pp7ws_list, pp8ws_list, pp9ws_list, pp10ws_list):
    """
    ppws -> percent previous winners selected
    """
    result_dict = {}

    result_dict["avg_ppws"] = mean(ppws_list)
    result_dict["avg_pp2ws"] = mean(pp2ws_list)
    result_dict["avg_pp3ws"] = mean(pp3ws_list)
    result_dict["avg_pp4ws"] = mean(pp4ws_list)
    result_dict["avg_pp5ws"] = mean(pp5ws_list)
    result_dict["avg_pp6ws"] = mean(pp6ws_list)
    result_dict["avg_pp7ws"] = mean(pp7ws_list)
    result_dict["avg_pp8ws"] = mean(pp8ws_list)
    result_dict["avg_pp9ws"] = mean(pp9ws_list)
    result_dict["avg_pp10ws"] = mean(pp10ws_list)

    result_dict["std_dev_ppws"] = stdev(ppws_list, xbar=result_dict["avg_ppws"])
    result_dict["std_dev_pp2ws"] = stdev(pp2ws_list, xbar=result_dict["avg_pp2ws"])
    result_dict["std_dev_pp3ws"] = stdev(pp3ws_list, xbar=result_dict["avg_pp3ws"])
    result_dict["std_dev_pp4ws"] = stdev(pp4ws_list, xbar=result_dict["avg_pp4ws"])
    result_dict["std_dev_pp5ws"] = stdev(pp5ws_list, xbar=result_dict["avg_pp5ws"])
    result_dict["std_dev_pp6ws"] = stdev(pp6ws_list, xbar=result_dict["avg_pp6ws"])
    result_dict["std_dev_pp7ws"] = stdev(pp7ws_list, xbar=result_dict["avg_pp7ws"])
    result_dict["std_dev_pp8ws"] = stdev(pp8ws_list, xbar=result_dict["avg_pp8ws"])
    result_dict["std_dev_pp9ws"] = stdev(pp9ws_list, xbar=result_dict["avg_pp9ws"])
    result_dict["std_dev_pp10ws"] = stdev(pp10ws_list, xbar=result_dict["avg_pp10ws"])

    result_dict["variance_ppws"] = variance(ppws_list, xbar=result_dict["avg_ppws"])
    result_dict["variance_pp2ws"] = variance(pp2ws_list, xbar=result_dict["avg_pp2ws"])
    result_dict["variance_pp3ws"] = variance(pp3ws_list, xbar=result_dict["avg_pp3ws"])
    result_dict["variance_pp4ws"] = variance(pp4ws_list, xbar=result_dict["avg_pp4ws"])
    result_dict["variance_pp5ws"] = variance(pp5ws_list, xbar=result_dict["avg_pp5ws"])
    result_dict["variance_pp6ws"] = variance(pp6ws_list, xbar=result_dict["avg_pp6ws"])
    result_dict["variance_pp7ws"] = variance(pp7ws_list, xbar=result_dict["avg_pp7ws"])
    result_dict["variance_pp8ws"] = variance(pp8ws_list, xbar=result_dict["avg_pp8ws"])
    result_dict["variance_pp9ws"] = variance(pp9ws_list, xbar=result_dict["avg_pp9ws"])
    result_dict["variance_pp10ws"] = variance(pp10ws_list, xbar=result_dict["avg_pp10ws"])

    return result_dict

def get_psfpl_stats(psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list, psfp5l_list,
    psfp6l_list, psfp7l_list, psfp8l_list, psfp9l_list, psfp10l_list):
    """
    psfpl -> percent selected from previous losers
    """
    result_dict = {}

    result_dict["avg_psfpl"] = mean(psfpl_list)
    result_dict["avg_psfp2l"] = mean(psfp2l_list)
    result_dict["avg_psfp3l"] = mean(psfp3l_list)
    result_dict["avg_psfp4l"] = mean(psfp4l_list)
    result_dict["avg_psfp5l"] = mean(psfp5l_list)
    result_dict["avg_psfp6l"] = mean(psfp6l_list)
    result_dict["avg_psfp7l"] = mean(psfp7l_list)
    result_dict["avg_psfp8l"] = mean(psfp8l_list)
    result_dict["avg_psfp9l"] = mean(psfp9l_list)
    result_dict["avg_psfp10l"] = mean(psfp10l_list)

    result_dict["std_dev_psfpl"] = stdev(psfpl_list, xbar=result_dict["avg_psfpl"])
    result_dict["std_dev_psfp2l"] = stdev(psfp2l_list, xbar=result_dict["avg_psfp2l"])
    result_dict["std_dev_psfp3l"] = stdev(psfp3l_list, xbar=result_dict["avg_psfp3l"])
    result_dict["std_dev_psfp4l"] = stdev(psfp4l_list, xbar=result_dict["avg_psfp4l"])
    result_dict["std_dev_psfp5l"] = stdev(psfp5l_list, xbar=result_dict["avg_psfp5l"])
    result_dict["std_dev_psfp6l"] = stdev(psfp6l_list, xbar=result_dict["avg_psfp6l"])
    result_dict["std_dev_psfp7l"] = stdev(psfp7l_list, xbar=result_dict["avg_psfp7l"])
    result_dict["std_dev_psfp8l"] = stdev(psfp8l_list, xbar=result_dict["avg_psfp8l"])
    result_dict["std_dev_psfp9l"] = stdev(psfp9l_list, xbar=result_dict["avg_psfp9l"])
    result_dict["std_dev_psfp10l"] = stdev(psfp10l_list, xbar=result_dict["avg_psfp10l"])

    result_dict["variance_psfpl"] = variance(psfpl_list, xbar=result_dict["avg_psfpl"])
    result_dict["variance_psfp2l"] = variance(psfp2l_list, xbar=result_dict["avg_psfp2l"])
    result_dict["variance_psfp3l"] = variance(psfp3l_list, xbar=result_dict["avg_psfp3l"])
    result_dict["variance_psfp4l"] = variance(psfp4l_list, xbar=result_dict["avg_psfp4l"])
    result_dict["variance_psfp5l"] = variance(psfp5l_list, xbar=result_dict["avg_psfp5l"])
    result_dict["variance_psfp6l"] = variance(psfp6l_list, xbar=result_dict["avg_psfp6l"])
    result_dict["variance_psfp7l"] = variance(psfp7l_list, xbar=result_dict["avg_psfp7l"])
    result_dict["variance_psfp8l"] = variance(psfp8l_list, xbar=result_dict["avg_psfp8l"])
    result_dict["variance_psfp9l"] = variance(psfp9l_list, xbar=result_dict["avg_psfp9l"])
    result_dict["variance_psfp10l"] = variance(psfp10l_list, xbar=result_dict["avg_psfp10l"])

    return result_dict

def get_psfpw_stats(psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list, psfp5w_list,
    psfp6w_list, psfp7w_list, psfp8w_list, psfp9w_list, psfp10w_list):
    """
    psfpw -> percent selected from previous winners
    """

    result_dict = {}

    result_dict["avg_psfpw"] = mean(psfpw_list)
    result_dict["avg_psfp2w"] = mean(psfp2w_list)
    result_dict["avg_psfp3w"] = mean(psfp3w_list)
    result_dict["avg_psfp4w"] = mean(psfp4w_list)
    result_dict["avg_psfp5w"] = mean(psfp5w_list)
    result_dict["avg_psfp6w"] = mean(psfp6w_list)
    result_dict["avg_psfp7w"] = mean(psfp7w_list)
    result_dict["avg_psfp8w"] = mean(psfp8w_list)
    result_dict["avg_psfp9w"] = mean(psfp9w_list)
    result_dict["avg_psfp10w"] = mean(psfp10w_list)

    result_dict["std_dev_psfpw"] = stdev(psfpw_list, xbar=result_dict["avg_psfpw"])
    result_dict["std_dev_psfp2w"] = stdev(psfp2w_list, xbar=result_dict["avg_psfp2w"])
    result_dict["std_dev_psfp3w"] = stdev(psfp3w_list, xbar=result_dict["avg_psfp3w"])
    result_dict["std_dev_psfp4w"] = stdev(psfp4w_list, xbar=result_dict["avg_psfp4w"])
    result_dict["std_dev_psfp5w"] = stdev(psfp5w_list, xbar=result_dict["avg_psfp5w"])
    result_dict["std_dev_psfp6w"] = stdev(psfp6w_list, xbar=result_dict["avg_psfp6w"])
    result_dict["std_dev_psfp7w"] = stdev(psfp7w_list, xbar=result_dict["avg_psfp7w"])
    result_dict["std_dev_psfp8w"] = stdev(psfp8w_list, xbar=result_dict["avg_psfp8w"])
    result_dict["std_dev_psfp9w"] = stdev(psfp9w_list, xbar=result_dict["avg_psfp9w"])
    result_dict["std_dev_psfp10w"] = stdev(psfp10w_list, xbar=result_dict["avg_psfp10w"])

    result_dict["variance_psfpw"] = variance(psfpw_list, xbar=result_dict["avg_psfpw"])
    result_dict["variance_psfp2w"] = variance(psfp2w_list, xbar=result_dict["avg_psfp2w"])
    result_dict["variance_psfp3w"] = variance(psfp3w_list, xbar=result_dict["avg_psfp3w"])
    result_dict["variance_psfp4w"] = variance(psfp4w_list, xbar=result_dict["avg_psfp4w"])
    result_dict["variance_psfp5w"] = variance(psfp5w_list, xbar=result_dict["avg_psfp5w"])
    result_dict["variance_psfp6w"] = variance(psfp6w_list, xbar=result_dict["avg_psfp6w"])
    result_dict["variance_psfp7w"] = variance(psfp7w_list, xbar=result_dict["avg_psfp7w"])
    result_dict["variance_psfp8w"] = variance(psfp8w_list, xbar=result_dict["avg_psfp8w"])
    result_dict["variance_psfp9w"] = variance(psfp9w_list, xbar=result_dict["avg_psfp9w"])
    result_dict["variance_psfp10w"] = variance(psfp10w_list, xbar=result_dict["avg_psfp10w"])

    return result_dict

def get_psfip_stats(psfip2_list, psfip3_list, psfip4_list, psfip5_list,
    psfip6_list, psfip7_list, psfip8_list, psfip9_list, psfip10_list):
    """
    psfip -> persent selected from intersect previous losers
    """

    result_dict = {}

    result_dict["avg_psfip2"] = mean(psfip2_list)
    result_dict["avg_psfip3"] = mean(psfip3_list)
    result_dict["avg_psfip4"] = mean(psfip4_list)
    result_dict["avg_psfip5"] = mean(psfip5_list)
    result_dict["avg_psfip6"] = mean(psfip6_list)
    result_dict["avg_psfip7"] = mean(psfip7_list)
    result_dict["avg_psfip8"] = mean(psfip8_list)
    result_dict["avg_psfip9"] = mean(psfip9_list)
    result_dict["avg_psfip10"] = mean(psfip10_list)

    result_dict["std_dev_psfip2"] = stdev(psfip2_list, xbar=result_dict["avg_psfip2"])
    result_dict["std_dev_psfip3"] = stdev(psfip3_list, xbar=result_dict["avg_psfip3"])
    result_dict["std_dev_psfip4"] = stdev(psfip4_list, xbar=result_dict["avg_psfip4"])
    result_dict["std_dev_psfip5"] = stdev(psfip5_list, xbar=result_dict["avg_psfip5"])
    result_dict["std_dev_psfip6"] = stdev(psfip6_list, xbar=result_dict["avg_psfip6"])
    result_dict["std_dev_psfip7"] = stdev(psfip7_list, xbar=result_dict["avg_psfip7"])
    result_dict["std_dev_psfip8"] = stdev(psfip8_list, xbar=result_dict["avg_psfip8"])
    result_dict["std_dev_psfip9"] = stdev(psfip9_list, xbar=result_dict["avg_psfip9"])
    result_dict["std_dev_psfip10"] = stdev(psfip10_list, xbar=result_dict["avg_psfip10"])

    result_dict["variance_psfip2"] = variance(psfip2_list, xbar=result_dict["avg_psfip2"])
    result_dict["variance_psfip3"] = variance(psfip3_list, xbar=result_dict["avg_psfip3"])
    result_dict["variance_psfip4"] = variance(psfip4_list, xbar=result_dict["avg_psfip4"])
    result_dict["variance_psfip5"] = variance(psfip5_list, xbar=result_dict["avg_psfip5"])
    result_dict["variance_psfip6"] = variance(psfip6_list, xbar=result_dict["avg_psfip6"])
    result_dict["variance_psfip7"] = variance(psfip7_list, xbar=result_dict["avg_psfip7"])
    result_dict["variance_psfip8"] = variance(psfip8_list, xbar=result_dict["avg_psfip8"])
    result_dict["variance_psfip9"] = variance(psfip9_list, xbar=result_dict["avg_psfip9"])
    result_dict["variance_psfip10"] = variance(psfip10_list, xbar=result_dict["avg_psfip10"])

    return result_dict


def get_pipls_stats(pip2ls_list, pip3ls_list, pip4ls_list, pip5ls_list,
    pip6ls_list, pip7ls_list, pip8ls_list, pip9ls_list, pip10ls_list):
    """
    pipls -> percent intersect previous losers selected
    percent of the common losers that are selected as winners in current draw
    """
    result_dict = {}

    result_dict["avg_pip2ls"] = mean(pip2ls_list)
    result_dict["avg_pip3ls"] = mean(pip3ls_list)
    result_dict["avg_pip4ls"] = mean(pip4ls_list)
    result_dict["avg_pip5ls"] = mean(pip5ls_list)
    result_dict["avg_pip6ls"] = mean(pip6ls_list)
    result_dict["avg_pip7ls"] = mean(pip7ls_list)
    result_dict["avg_pip8ls"] = mean(pip8ls_list)
    result_dict["avg_pip9ls"] = mean(pip9ls_list)
    result_dict["avg_pip10ls"] = mean(pip10ls_list)

    result_dict["std_dev_pip2ls"] = stdev(pip2ls_list, xbar=result_dict["avg_pip2ls"])
    result_dict["std_dev_pip3ls"] = stdev(pip3ls_list, xbar=result_dict["avg_pip3ls"])
    result_dict["std_dev_pip4ls"] = stdev(pip4ls_list, xbar=result_dict["avg_pip4ls"])
    result_dict["std_dev_pip5ls"] = stdev(pip5ls_list, xbar=result_dict["avg_pip5ls"])
    result_dict["std_dev_pip6ls"] = stdev(pip6ls_list, xbar=result_dict["avg_pip6ls"])
    result_dict["std_dev_pip7ls"] = stdev(pip7ls_list, xbar=result_dict["avg_pip7ls"])
    result_dict["std_dev_pip8ls"] = stdev(pip8ls_list, xbar=result_dict["avg_pip8ls"])
    result_dict["std_dev_pip9ls"] = stdev(pip9ls_list, xbar=result_dict["avg_pip9ls"])
    result_dict["std_dev_pip10ls"] = stdev(pip10ls_list, xbar=result_dict["avg_pip10ls"])

    result_dict["variance_pip2ls"] = variance(pip2ls_list, xbar=result_dict["avg_pip2ls"])
    result_dict["variance_pip3ls"] = variance(pip3ls_list, xbar=result_dict["avg_pip3ls"])
    result_dict["variance_pip4ls"] = variance(pip4ls_list, xbar=result_dict["avg_pip4ls"])
    result_dict["variance_pip5ls"] = variance(pip5ls_list, xbar=result_dict["avg_pip5ls"])
    result_dict["variance_pip6ls"] = variance(pip6ls_list, xbar=result_dict["avg_pip6ls"])
    result_dict["variance_pip7ls"] = variance(pip7ls_list, xbar=result_dict["avg_pip7ls"])
    result_dict["variance_pip8ls"] = variance(pip8ls_list, xbar=result_dict["avg_pip8ls"])
    result_dict["variance_pip9ls"] = variance(pip9ls_list, xbar=result_dict["avg_pip9ls"])
    result_dict["variance_pip10ls"] = variance(pip10ls_list, xbar=result_dict["avg_pip10ls"])

    return result_dict

def get_remaining_nums_stats(prns_list, psfrn_list, draws_per_round_list):
    """

    """
    result_dict = {}

    result_dict["avg_prns"] = mean(prns_list)
    result_dict["avg_psfrn"] = mean(psfrn_list)
    result_dict["avg_draws_per_round"] = mean(draws_per_round_list)

    result_dict["std_dev_prns"] = stdev(prns_list, xbar=result_dict["avg_prns"])
    result_dict["std_dev_psfrn"] = stdev(psfrn_list, xbar=result_dict["avg_psfrn"])
    result_dict["std_dev_draws_per_round"] = stdev(draws_per_round_list, xbar=result_dict["avg_draws_per_round"])

    result_dict["variance_prns"] = variance(prns_list, xbar=result_dict["avg_prns"])
    result_dict["variance_psfrn"] = variance(psfrn_list, xbar=result_dict["avg_psfrn"])
    result_dict["variance_draws_per_round"] = variance(draws_per_round_list, xbar=result_dict["avg_draws_per_round"])

    return result_dict

def get_plirn_stats(pip2lrns_list, psfip2lrn_list):
    """
    Plirn -> percent losers intersect remaining nums stats
    """
    result_dict = {}

    result_dict["avg_pip2lrns"] = mean(pip2lrns_list)
    result_dict["avg_psfip2lrn"] = mean(psfip2lrn_list)

    result_dict["std_dev_pip2lrns"] = stdev(pip2lrns_list, xbar=result_dict["avg_pip2lrns"])
    result_dict["std_dev_psfip2lrn"] = stdev(psfip2lrn_list, xbar=result_dict["avg_psfip2lrn"])

    result_dict["variance_pip2lrns"] = variance(pip2lrns_list, xbar=result_dict["avg_pip2lrns"])
    result_dict["variance_psfip2lrn"] = variance(psfip2lrn_list, xbar=result_dict["avg_psfip2lrn"])

    return result_dict

def get_draw_distance_dict_list_stats(draw_distance_dict):
    """
    input: draw_distance_dict with list of nums as values
    return: dict of avg of list values for all keys
    """

    ret_dict = dict()

    for spot in draw_distance_dict.keys():
        if(len(draw_distance_dict[spot]) > 2):
            ret_dict[spot] = dict()

            stats_dict = dict()
            stats_dict["avg"] = mean(draw_distance_dict[spot])
            stats_dict["std_dev"] = stdev(draw_distance_dict[spot], stats_dict["avg"])
            stats_dict["variance"] = variance(draw_distance_dict[spot], stats_dict["avg"])
            stats_dict["max"] = max(draw_distance_dict[spot])
            stats_dict["min"] = min(draw_distance_dict[spot])


            ret_dict[spot] = stats_dict

    return ret_dict


#check percent of time, that a number with higher mod number in previous set will appear less in current set
#get list of mod values in draw order num
#get
prev_set_mod_mode = None
prev_round_set = None
