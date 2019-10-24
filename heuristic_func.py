import math as math
from drawing_set_stats import update_remaining_nums_set
import init_functions as init
import assist_funcs as assist
from time import sleep
import heuristic_function_stats as heuristic_stats
import file_reading_funcs as read

#functions for heuristics for confidence values
BASE_CONF = 25
LAST_DRAW_WINNER_CONF = 25
LAST_DRAW_LOSER_CONF = 75
INTER_DRAW_AVG = 4
AVG_SELECTION_RATE = float(1/4)

WINNING_SPOT_AVG = 40
WINNING_SPOT_STD_DEV = 3.5

HIGH_AVG_CONF = 2.5
MID_AVG_CONF = 1

LAST_N_DRAW_NUM_CONF = 1
LAST_N_EXCEED_MAX_CONF = 250

ROUND_COUNT_CONF = 40

LAST_N_VAL = 15

MAX_DRAW_DISTANCE = 26
DRAW_DISTANCE_AVG = 4

LONGEST_DRAW_DISTANCE_CONF = 50
LONGEST_N_DRAW_DISTANCE_SPOTS = 8

#Conf based on appearance of appearance percentages
DRAW_DIST_1_CONF = 25
DRAW_DIST_2_CONF = 18
DRAW_DIST_3_CONF = 14
DRAW_DIST_4_CONF = 10


CURRENT_DRAW_DISTANCE_CONFIDENCE_DICT = {
    1 : (DRAW_DIST_1_CONF * 2.5),
    2 : (DRAW_DIST_2_CONF * 2.5),
    3 : (DRAW_DIST_3_CONF * 2.5),
    4 : (DRAW_DIST_4_CONF * 2.5)
}

milestone_dict = read.read_dict_from_file("milestone_dict")

#nested dict[spot_key][distance_key] = confidence points that the number will be selected in that many draws
spot_distance_confidence_dict = init.init_nested_dict(init.spot_key_list, [*range(1, MAX_DRAW_DISTANCE)])

#dict that holds values of avg draw distances of last n draws
# keys: 2-16
# 0.8, 0.7, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2
# values: 2.0, 1.8, 1.6, 1.5, 1.2, 1.2, 1.1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.75, .6                   2     3    4    5   6     7     8    9    10    11    12    13    14    15   16
last_n_draw_distance_avg_std_dev_dict = init.init_dict(init.get_last_n_avg_key_list(LAST_N_VAL + 1), [0.8, 0.7, 0.6, 0.6, 0.5, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2])
print(last_n_draw_distance_avg_std_dev_dict)

def get_summation_of_prev_draw_confidences(spot_key, draw_distance):
    """
    input: spot number, draw_distance
    return confidence as a summation of current + all previous draws in spot_distance_confidence_dict
    """

    draw_count = 1
    confidence_points = 0

    while(draw_count <= draw_distance):
        confidence_points += spot_distance_confidence_dict[spot_key][draw_count]
        draw_count += 1

    return confidence_points

def reset_nested_confidence_dict_vals(nested_confidence_dict):
    for outer_key in nested_confidence_dict.keys():
        reset_spot_confidence_dict(nested_confidence_dict[outer_key])


def reset_spot_confidence_dict(confidence_dict):
    for key in confidence_dict.keys():
        confidence_dict[key] = 0

def add_val_to_dict_key_list(spot_confidence_dict, dict_key_list, val):
    """
    spot_confidence_dict[key in key list] += val
    """

    for key in dict_key_list:
        spot_confidence_dict[key] += val

def get_current_draw_distance_dict(last_seen_dict, current_draw_num):
    current_draw_dist_dict = dict()

    for spot_key in last_seen_dict.keys():
        current_draw_dist_dict[spot_key] = abs(current_draw_num - last_seen_dict[spot_key]) + 1

    return current_draw_dist_dict


def get_confidence_values(spot_confidence_dict, last_seen_dict=None, winning_sets_list=None, losing_sets_list=None,
    spot_histogram=None, num_draws_sampled=None, current_draw_num=None, draw_distance_dict=None,
    remaining_nums_set=None, num_draws_in_round=None, last_n_avg_distance_dict=None,
    prev_means_list=None):
    """
    Get spot_confidence values based on heuristic functions
    """
    #first reset dict
    reset_spot_confidence_dict(spot_confidence_dict)
    current_draw_dist_dict = None

    if(last_seen_dict is not None and current_draw_num is not None):
        current_draw_dist_dict = get_current_draw_distance_dict(last_seen_dict, current_draw_num)
    #
    # if(len(winning_sets_list) > 1):
    #     print("Prev winner:", winning_sets_list[-1])
    #     add_val_to_dict_key_list(spot_confidence_dict, winning_sets_list[-1], 100)

    # print("Gettings avg means heuristic...")
    # last_n_means_heuristic(spot_confidence_dict, prev_means_list)

    # print("Getting long previous draw heuristic...")
    # long_prev_draw_distance_heuristic(spot_confidence_dict, last_seen_dict, draw_distance_dict, current_draw_num)

    # print("Getting current draw distance heuristic...")
    # current_draw_distance_heuristic(spot_confidence_dict, last_seen_dict, current_draw_num)

    #heuristic based on most common draw distances and on avg numbers will be selected amongst 4 draws
    # common_draw_distance_heuristic(spot_confidence_dict, last_seen_dict, current_draw_num)

    if(current_draw_dist_dict is not None):
        # print("Getting low draw distance avg heuristic...")
        # low_draw_dist_avg_heuristic(spot_confidence_dict, current_draw_dist_dict, draw_distance_dict)

        print("Getting long prev draw distance heuristic...")
        long_prev_draw_distance_heuristic(spot_confidence_dict, current_draw_dist_dict, draw_distance_dict)

    # print("Getting Min max mode heuristic...")
    min_max_mode_heuristic(spot_confidence_dict, spot_histogram)
    #
    # common_draw_distance_heuristic(spot_confidence_dict, current_draw_dist_dict)

    #
    #
    # # remaining nums heuuristic
    # # take current draw set and remove from remaining nums set
    # if(remaining_nums_set is not None and num_draws_sampled is not None):
    #     #update remaining nums set
    #     print("Updating remaining nums set...")
    #     print("Remaining nums set:", remaining_nums_set)
    #     print("Current draw set:", winning_sets_list[-1])
    #
    #     # remaining_nums_dict = update_remaining_nums_set(remaining_nums_set=remaining_nums_set, num_draws_in_round=num_draws_in_round, current_draw_set=winning_sets_list[-1])
    #     #
    #     # remaining_nums_set = remaining_nums_dict["remaining_nums_set"]
    #     # num_draws_in_round = remaining_nums_dict["num_draws_in_round"]
    #     #
    #     # print("After updating remaining nums set...")
    #     # print("Remaining nums set:", remaining_nums_set)
    #     # print("Num draws in round:", num_draws_in_round)
    #
    #     print("Getting round number heuristic...")
    #     remaining_nums_in_round_heuristic(spot_confidence_dict, remaining_nums_set, num_draws_in_round)


    # longest_draw_distance_heuristic(spot_confidence_dict, last_seen_dict, current_draw_num)

    #confidence placed on draw distance, assign confidence by getting confidence for current draw
    sorted_spot_confidence_dict = assist.get_sorted_dict(spot_confidence_dict)
    print(sorted_spot_confidence_dict)
    return sorted_spot_confidence_dict


def get_expected_count_in_period(num_draws):
    """
    return expected number of selections each number should have at the current
    num spots sampled
    """

    return AVG_SELECTION_RATE * (num_draws)

def get_poisson_labda_val(num_draws):
    return get_expected_count_in_period(num_draws)

def min_max_mode_heuristic(spot_confidence_dict, spot_histogram):
    """
    Heuristic assigns more confidence to top 5 most selected values
    Reduce confidence on the top 5 least selected values
    """
    add_confidence = 25
    neg_confidence = -25

    ordered_key_list = assist.get_sorted_key_list(spot_histogram)

    #ordered from least spot count to most spot count
    add_val_to_dict_key_list(spot_confidence_dict, ordered_key_list[:5], neg_confidence)
    add_val_to_dict_key_list(spot_confidence_dict, ordered_key_list[-5:], add_confidence)

# def expected_draw_distance():
#     # for every day use n_wins_expect value to get avg and std_dev for all n_wins_key



def update_spot_distance_confidence(spot_key, draw_distance, n_val):
    global spot_distance_confidence_dict
    spot_distance_confidence_dict[spot_key][draw_distance] += (LAST_N_DRAW_NUM_CONF * n_val)
    # print("spot_distance_confidence_dict[" , spot_key, "][", draw_distance, "] +=",  (LAST_N_DRAW_NUM_CONF * n_val), "confidence")

def assign_draw_distance_confidence(spot_key, last_n_avg_distance_dict, n_val):
    """
    Assign confidence to number of draws till next selection
    Based on avg draw distance avgs and standard deviations for avg draw distances
    Assign more confidence to draw distances where, those draw distances added to current
    sum >= avg - std_dev and <= avg + std_dev
    """
    #get the upper and lower bound for the next n_val, to check if the draw_distance
    #added to sum stays in bound of next n_val
    next_lower_bound = DRAW_DISTANCE_AVG - last_n_draw_distance_avg_std_dev_dict[n_val + 1]
    next_upper_bound = DRAW_DISTANCE_AVG + last_n_draw_distance_avg_std_dev_dict[n_val + 1]


    if(last_n_avg_distance_dict[n_val] is not None and last_n_avg_distance_dict[n_val] != 0):
        # print("N_key_val:", n_val)
        # print(last_n_avg_distance_dict)

        #get total
        sum_val = last_n_avg_distance_dict[n_val] * n_val
        avg_too_high = False
        # print(sum_val)

        #count for the draw numbers to assing confidence to draw distances
        draw_count = 1

        #stop looking for draws when sum_val + draw_count avg is too high
        while(not avg_too_high):
            next_avg = (sum_val + draw_count) / (n_val + 1)
            if(next_avg < next_lower_bound or next_avg > next_upper_bound):
                #don't assign confidence values
                if(next_avg < next_lower_bound):
                    #if getting values lower than avg continue getting draw counts
                    draw_count += 1
                    continue
                else:
                    #if we are on the first draw and avg still too high
                    #add confidence to 1 and 2  draw_distance

                    if(draw_count == 1):
                        # print("Avg too high. Adding confidence to (1,2, 3)...")
                        update_spot_distance_confidence(spot_key, draw_count, n_val)
                        update_spot_distance_confidence(spot_key, draw_count + 1, n_val)
                        update_spot_distance_confidence(spot_key, draw_count + 2, n_val)

                    avg_too_high = True

            else:
                #next avg falls within our bounds
                #add confidence to draw_distance count
                #in dict
                if(draw_count < MAX_DRAW_DISTANCE):
                    # print("Spot_key:", spot_key, "Draw distance:", draw_count, " within bounds", next_lower_bound, " -", next_upper_bound)
                    update_spot_distance_confidence(spot_key, draw_count, n_val)
                else:
                    avg_too_high =  True

            draw_count += 1

        # print(spot_distance_confidence_dict[spot_key])


# spot_confidence_dict, draw_distance_dict, last_n_avg_distance_dict
def avg_draw_distance_heuristic(spot_confidence_dict, last_n_avg_distance_dict, winning_sets_list, last_seen_dict, current_draw_num):
    #for each spot get last_n_avg draw distances
    #confidence val based on distance from 0 * spot_key
    # print("Last n avg distance dict:")
    # print(last_n_avg_distance_dict)
    global spot_distance_confidence_dict

    #update avg values for most recent winning set
    for spot_key in winning_sets_list[-1]:
        #reset the confidence in the number of draws
        reset_spot_confidence_dict(spot_distance_confidence_dict[spot_key])

        spot_last_n_avg_distance_dict = last_n_avg_distance_dict[spot_key]

        # print("Spot_key:", spot_key, "\nDraw Distance Avg List:\n", spot_last_n_avg_distance_dict)

        for n_key in spot_last_n_avg_distance_dict.keys():
            if(spot_last_n_avg_distance_dict[n_key] is not None and spot_last_n_avg_distance_dict[n_key] != 0):
                assign_draw_distance_confidence(spot_key, last_n_avg_distance_dict[spot_key], n_key)



    #let num confidence points be summation of all confidence in draws upto current draw distance
    for spot_key in spot_confidence_dict.keys():
        draw_distance = abs(current_draw_num - last_seen_dict[spot_key])
        #get confidence points of the next draw distance
        confidence_points = None
        if(draw_distance + 1 < MAX_DRAW_DISTANCE):
            # confidence_points = get_summation_of_prev_draw_confidences(spot_key, draw_distance + 1)
            confidence_points = spot_distance_confidence_dict[spot_key][draw_distance + 1]
        else:
            #assign a large base confidence since current draw distance is larger than max measured distances
            #can expect the number to appear soon
            confidence_points = LAST_N_EXCEED_MAX_CONF



        spot_confidence_dict[spot_key] += confidence_points


def last_n_means_heuristic(spot_confidence_dict, prev_means_list):
    """
    Avg for winning spots is centered around 40 in long running avg
    Place confidence vals based on last_n_avgs
    """

    #assign confidence based on the last draw avg
    #last 5 draws avg
    #last 10 draws avg
    #last 15 draws avg

    if(len(prev_means_list) < 3):
        return

    confidence_points = 50

    #if previous avg is greater than avg+std_dev
    #confidence to lower numbers and expect lower avg
    #unless prev[-2] value is < avg-std_dev, forcing previous value high
    # if(not prev_means_list[-2] < (WINNING_SPOT_AVG - WINNING_SPOT_STD_DEV)):
    #     if(prev_means_list[-1] > (WINNING_SPOT_AVG + WINNING_SPOT_STD_DEV)):
    #         print("Avg:", prev_means_list[-1], "adding", confidence_points, "to 1-30")
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(1, 31)], confidence_points)
    #
    #     if(prev_means_list[-2] > (WINNING_SPOT_AVG + WINNING_SPOT_STD_DEV)):
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(1, 31)], confidence_points)
    #
    #
    # #add confidence to higher numbers if avg is high
    # #unless prev[-2] avg is high, forcing prev[-1] avg to be low
    # if(not prev_means_list[-2] > (WINNING_SPOT_AVG + WINNING_SPOT_STD_DEV)):
    #     if(prev_means_list[-1] < (WINNING_SPOT_AVG - WINNING_SPOT_STD_DEV)):
    #         print("Avg:", prev_means_list[-1], "adding", confidence_points, "to 50-80")
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(50, 81)], confidence_points)
    #
    #
    #     if(prev_means_list[-2] < (WINNING_SPOT_AVG - WINNING_SPOT_STD_DEV)):
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(50, 81)], confidence_points)



    # get avg of means for last 5 draws
    last_n_means_dict = assist.get_last_n_avg_dict(prev_means_list, [3])
    print(last_n_means_dict)

    for n_key in last_n_means_dict.keys():
        if(last_n_means_dict[n_key] is not None):
            if(last_n_means_dict[n_key] > WINNING_SPOT_AVG + 2.5):
                print("Avg:", last_n_means_dict[n_key], "adding", confidence_points, "to 1-30")
                add_val_to_dict_key_list(spot_confidence_dict, [*range(1, 11)], confidence_points)
            elif (last_n_means_dict[n_key] < WINNING_SPOT_AVG - 2.5):
                print("Avg:", last_n_means_dict[n_key], "adding", confidence_points, "to 50-80")
                add_val_to_dict_key_list(spot_confidence_dict, [*range(70, 81)], confidence_points)


    #get avg over the last 2


    # for n_key in last_n_means_dict.keys():
    #
    #     dev = WINNING_SPOT_AVG - last_n_means_dict[n_key]
    #     confidence_points = abs(dev) * n_key / 2
    #
    #     #last_n_avg > WINNING_SPOT_AVG
    #     #put confidence in spots 1-30
    #     if(dev < 0):
    #         print("Avg:", last_n_means_dict[n_key], "N_Key:", n_key, "Dev:", dev, "adding", confidence_points, "to 1-30")
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(1, 31)], confidence_points)
    #     elif(dev > 0):
    #         print("Avg:", last_n_means_dict[n_key], "N_Key:", n_key, "Dev:", dev, "adding", confidence_points, "to 50-80")
    #         #put confidence in spots 50-80
    #         add_val_to_dict_key_list(spot_confidence_dict, [*range(50, 81)], confidence_points)

def remaining_nums_in_round_heuristic(spot_confidence_dict, remaining_nums_set, current_round_num):
    #give confidence to spots that havent been selected, expect 5 percent of numbers to be selected by the
    #round length to get to less than 5 items in remaining nums set in 7-9 draws
    if(current_round_num >= 7):
        #put confidence on all nums in set
        for spot_key in remaining_nums_set:
            spot_confidence_dict[spot_key] += ROUND_COUNT_CONF


def long_prev_draw_distance_heuristic(spot_confidence_dict, current_draw_distance_dict, draw_distance_lists_dict):
    """
    input: spot confidence dict, prev_draw_distance_dict)
    heuristic based on if there is a number with a larger draw distance (ex: > 8)
    on previous draw, the next draw for that number is either within first few draws (1, 2, 3)
    or larger draw distances (> 8)
    """

    add_confidence = 50
    neg_confidence = 25

    for spot in spot_confidence_dict.keys():
        if(draw_distance_lists_dict[spot][-1] >= 8):
            if(current_draw_distance_dict[spot] <= 2):
                spot_confidence_dict[spot] += add_confidence
            else:
                spot_confidence_dict[spot] -= neg_confidence

        if(draw_distance_lists_dict[spot][-2] >= 8):
            if(current_draw_distance_dict[spot] <= 2):
                spot_confidence_dict[spot] += add_confidence
            else:
                spot_confidence_dict[spot] -= neg_confidence

def low_draw_dist_avg_heuristic(spot_confidence_dict, current_draw_distance_dict, draw_distance_lists_dict):
    add_confidence = 50
    neg_confidence = 25

    low_avg_dict = init.init_spot_dict()

    for spot in draw_distance_lists_dict.keys():
        draw_distance_list = draw_distance_lists_dict[spot]
        last_n_avg = assist.get_last_n_avg(draw_distance_list, 2)

        if(last_n_avg is not None):
            low_avg_dict[spot] = last_n_avg

            #if low avg expect more recent draw appearance
            if(last_n_avg < 2.2):
                if(current_draw_distance_dict[spot] <= 2):
                    print("Adding confidence spot:", spot)
                    spot_confidence_dict[spot] += add_confidence
                else:
                    print("Neg confidence spot:", spot)
                    spot_confidence_dict[spot] -= neg_confidence

    print(assist.get_sorted_dict(low_avg_dict))


def common_draw_distance_heuristic(spot_confidence_dict, current_draw_distance_dict):
    for spot_key, current_dist in current_draw_distance_dict.items():
        if(current_dist <= len(CURRENT_DRAW_DISTANCE_CONFIDENCE_DICT)):
            print("Spot:", spot_key, "dist:", current_dist)
            spot_confidence_dict[spot_key] += CURRENT_DRAW_DISTANCE_CONFIDENCE_DICT[current_dist]
