import assist_funcs as assist
from time import sleep

FIRST_SPOT = 1
LAST_SPOT = 80

spot_key_list = [*range(1, 81)]

def get_last_n_avg_key_list(n):
    return [*range(2, n+1)]

def init_dict(key_list, val_list=None):
    """
    initialize dict with keys from key list
    init all keys to 0
    """
    ret_dict = dict()

    val_index = 0

    for key in key_list:
        if(val_list is None):
            ret_dict[key] = 0
        else:
            if(val_index < len(val_list)):
                ret_dict[key] = val_list[val_index]
                val_index += 1
            else:
                ret_dict[key] = 0

    return ret_dict


def init_spot_dict():
    """
    input: any empty dict
    makes dict with keys from 1-80, set value to 0
    """
    return init_dict(spot_key_list)

def init_spot_dict_val(val):
    """
    return spot dict with keys and val=val
    """
    ret_dict = dict()

    for i in range(1, 81):
        ret_dict[i] = val

    return ret_dict

def init_range_set():
    ret_set = set()
    for i in range(1, 81):
        ret_set.add(i)

    return ret_set

def init_range_histogram():

    ret_dict = {
        "1-10" : 0,
        "11-20" : 0,
        "21-30" : 0,
        "31-40" : 0,
        "41-50" : 0,
        "51-60" : 0,
        "61-70" : 0,
        "71-80" : 0,
    }

    return ret_dict

def init_set_lists(winning_sets_list, losing_sets_list, winning_intersect_list,
    losing_intersect_list, prev_draws_mean_list, num_prev_draws,
    num_spots_sampled, spot_histogram=None, range_histogram=None,
        last_seen_dict=None, avg_draw_distance_dict=None,
        draw_distance_dict=None, last_n_avg_distance_dict=None,
        remaining_nums_set=None, num_draws_in_round=None,
        spot_confidence_dict=None,
        last_n_means_dict=None):
    """
    initialize starting lists and dicts to get good data basis
    gets upto n prev_draws and data in input lists
    return dict {current_draw_num, num_spots_sampled, num_draws_sampled}
    """
    import past_draws_stats as pds
    import drawing_set_stats as dss
    from heuristic_func import get_confidence_values
    from heuristic_function_stats import get_heuristic_stats
    from heuristic_function_stats import get_last_n_guessed_correct

    # print(last_n_avg_distance_dict)

    #start getting current draw
    current_winner_dict = pds.get_most_recent_draw(last_seen_dict=last_seen_dict, first_draw=True)
    print(current_winner_dict)

    most_recent_draw_num = current_winner_dict["draw_num"]
    current_draw_num = most_recent_draw_num - num_prev_draws
    # winning_sets_list.append(current_winner_dict["spot_set"])
    # losing_sets_list.append(dss.get_losers_for_draw_set(current_winner_dict["spot_set"]))
    # prev_draws_mean_list.append(current_winner_dict["mean"])

    #init last_seen_dict to starting draw
    for key in last_seen_dict.keys():
        last_seen_dict[key] = current_draw_num

    # print(last_seen_dict)

    num_draws_sampled = 0

    #get num_prev_draws of previous draws
    i = 0

    while(i < num_prev_draws):
        draw_results_dict = pds.get_results_from_draw_num(current_draw_num + i, num_spots_sampled=num_spots_sampled,
            spot_histogram=spot_histogram, range_histogram=range_histogram,
            last_seen_dict=last_seen_dict, avg_draw_distance_dict=avg_draw_distance_dict,
            draw_distance_dict=draw_distance_dict, last_n_avg_distance_dict = last_n_avg_distance_dict)


        winning_sets_list.append(draw_results_dict["spot_set"])
        losing_sets_list.append(dss.get_losers_for_draw_set(draw_results_dict["spot_set"]))
        prev_draws_mean_list.append(draw_results_dict["mean"])

        #get the means list for past 15 draws
        # if(len(prev_draws_mean_list) > 15):
        #     last_n_means_dict = assist.get_last_n_avg_dict(prev_draws_mean_list, get_last_n_avg_key_list(pds.last_n))
        #     print(last_n_means_dict)

        print(draw_results_dict)
        print(winning_sets_list[-1])
        # sleep(2)

        #keep winning sets list limit to past 10 sets
        #shift new values in
        if(len(winning_sets_list) >= 15):
            assist.shift_left_list(winning_sets_list, draw_results_dict["spot_set"])
            assist.shift_left_list(losing_sets_list, dss.get_losers_for_draw_set(draw_results_dict["spot_set"]))

        #update the remaining_nums_set

        if(remaining_nums_set is not None and num_draws_in_round is not None):
            remaining_num_dict = assist.update_remaining_nums_set(remaining_nums_set=remaining_nums_set, current_draw_set=draw_results_dict["spot_set"],
                num_draws_in_round=num_draws_in_round, current_draw_num=current_draw_num + i)

            remaining_nums_set = remaining_num_dict["remaining_nums_set"]
            num_draws_in_round = remaining_num_dict["num_draws_in_round"]

            if(num_draws_in_round == 0):
                #new round started
                print("New round started.")

            # print(remaining_nums_set)


        #check heuristic functions
        if(spot_confidence_dict is not None):
            print("Getting num guessed correctly...")
            get_last_n_guessed_correct(winning_sets_list[-1], assist.get_sorted_dict(spot_confidence_dict))

            get_confidence_values(spot_confidence_dict, last_seen_dict=last_seen_dict,
                winning_sets_list=winning_sets_list, losing_sets_list=losing_sets_list,
                spot_histogram=spot_histogram, num_draws_sampled=num_draws_sampled, current_draw_num=current_draw_num + i,
                draw_distance_dict=draw_distance_dict,
                remaining_nums_set=remaining_nums_set,
                num_draws_in_round=num_draws_in_round,
                last_n_avg_distance_dict=last_n_avg_distance_dict,
                prev_means_list=prev_draws_mean_list)




        i += 1
        num_draws_sampled += 1

        print("Num draws sampled:", num_draws_sampled)

    get_heuristic_stats()

    #check if the current draw num has changed from when last checked
    current_winner_dict = pds.get_most_recent_draw()
    print("Current draw num:", current_draw_num)
    print(current_winner_dict)

    diff_in_draws = abs(current_winner_dict["draw_num"] - most_recent_draw_num)

    print("Checking if another draw has passed...")
    print(current_winner_dict["draw_num"])
    print(most_recent_draw_num)

    if(diff_in_draws != 0):
        print("Getting next draw...")
        i = 1
        while(i <= diff_in_draws):
            draw_results_dict = pds.get_results_from_draw_num(current_draw_num + i, num_spots_sampled=num_spots_sampled,
                spot_histogram=spot_histogram, range_histogram=range_histogram,
                last_seen_dict=last_seen_dict, avg_draw_distance_dict=avg_draw_distance_dict,
                draw_distance_dict=draw_distance_dict, last_n_avg_distance_dict = last_n_avg_distance_dict)

            winning_sets_list.append(draw_results_dict["spot_set"])
            losing_sets_list.append(dss.get_losers_for_draw_set(draw_results_dict["spot_set"]))
            prev_draws_mean_list.append(draw_results_dict["mean"])

            #keep winning sets list limit to past 10 sets
            #shift new values in
            if(len(winning_sets_list) >= 15):
                assist.shift_left_list(winning_sets_list, draw_results_dict["spot_set"])
                assist.shift_left_list(losing_sets_list, dss.get_losers_for_draw_set(draw_results_dict["spot_set"]))


            #update the remaining_nums_set
            if(remaining_nums_set is not None and num_draws_in_round is not None):
                remaining_num_dict = assist.update_remaining_nums_set(remaining_nums_set=remaining_nums_set, current_draw_set=draw_results_dict["spot_set"],
                    num_draws_in_round=num_draws_in_round, current_draw_num=current_draw_num)

                if(num_draws_in_round == 0):
                    #new round started
                    print("New round started.")

            i += 1
            num_prev_draws += 1

            #get most recent draw



    current_draw_num = current_winner_dict["draw_num"]

    #set the intersect lists
    init_intersect_sets(losing_intersect_list, losing_sets_list)
    init_intersect_sets(winning_intersect_list, winning_sets_list)

    ret_dict = {
        "starting_draw_num" : current_draw_num - (num_prev_draws),
        "current_draw_num" : current_draw_num,
        "num_spots_sampled" : (num_prev_draws + 1)*20 ,
        "num_draws_sampled" : num_prev_draws + 1,
    }

    return ret_dict

    # ("Intersect lists:")
    # print(winning_intersect_list)
    # print(losing_intersect_list)

def init_intersect_sets(intersect_set_list, set_list):
    """
    input: empty intersect_set_list, set_list (non empty)
    Let each index be an intersect of values from previous indexes in
    set_list
    """

    if(len(set_list) < 3):
        print("Error: Size of input set list must be >= 2")
        return

    #start at second index
    #-1th index has winners/losers of current draw
    i = len(set_list) - 1

    while(i > 0):
        if(len(intersect_set_list) == 0):
            #no values save first intersect
            intersect_set_list.append(set_list[i].intersection(set_list[i-1]))
        else:
            #save intersect between prev intersect value and ith set in set_list

            #if prev intersect set is empty
            #no more intersects can be made so return
            if(len(intersect_set_list[-1]) == 0):
                #remove the empty set from the list
                intersect_set_list.pop()
                return

            intersect_set_list.append(intersect_set_list[-1].intersection(set_list[i]))

        i -= 1

    print(intersect_set_list)

def init_dict_list(key_list):
    ret_dict = dict()

    for key in key_list:
        ret_dict[key] = list()

    return ret_dict

def init_spot_dict_list():
    """
    return dict with keys from 1-80, set value to empty list
    """
    # for i in range(1, 81):
    #     empty_dict[i] = list()
    return init_dict_list(spot_key_list)


def init_dict_dict_list(key_list_outer, key_list_inner):
    #for each spot make a dict
    ret_dict = dict()

    for outer_key in key_list_outer:
        ret_dict[outer_key] = dict()

        for inner_key in key_list_inner:
            ret_dict[outer_key][inner_key] = list()

    return ret_dict


def init_spot_dict_dict_list(inner_dict_list_size):
    """
    input: empty dict
    makes a dict such that
    dict[spot_num][n] = list avg of last n elements of draw_distance_dict for the spot_num
    """
    # # Create a list in a range of 10-20
    # My_list = [*range(10, 21, 1)]

    return init_dict_dict_list(spot_key_list, get_last_n_avg_key_list(inner_dict_list_size))

    # print(empty_dict)

def init_nested_dict(outer_dict_key_list, inner_dict_key_list):
    """
    input: outer dict key list, inner dict key list
    return: nested dict
    """

    ret_dict = dict()

    for outer_key in outer_dict_key_list:
        ret_dict[outer_key] = dict()

        for inner_key in inner_dict_key_list:
            ret_dict[outer_key][inner_key] = 0

    return ret_dict

def init_nested_nested_dict(outer_dict_key_list, inner_dict_key_list):
    """
    input: empty_dict, first dict size, nested dict size
    makes empty_dict with 1->num_keys1 and 2 -> inner_num_keys len
    """

    ret_dict = dict()

    for outer_key in outer_dict_key_list:
        ret_dict[outer_key] = dict()

        for inner_key in inner_dict_key_list:
            ret_dict[outer_key][inner_key] = dict()

    # print(empty_dict)
    return ret_dict
