# from past_draws_stats import get_most_recent_draw
# from past_draws_stats import get_results_from_draw_num
#
# from past_draws_stats import spot_histogram
# from past_draws_stats import range_histogram
# from past_draws_stats import last_seen_dict
# from past_draws_stats import starting_draw_num
import statistics as stats
import operator

def get_list_stats(any_list):
    #get stats
    ret_dict = {}

    ret_dict["avg"] = stats.mean(any_list)
    ret_dict["std_dev"] = stats.stdev(any_list, xbar=ret_dict["avg"])
    ret_dict["variance"] = stats.variance(any_list, xbar=ret_dict["avg"])
    ret_dict["max"] = max(any_list)
    ret_dict["min"] = min(any_list)
    ret_dict["median"] = stats.median(any_list)

    #for mode round every avg
    real_mode = max(set(any_list), key=any_list.count)

    round_val_list = [round(x) for x in any_list]

    rounded_mode = max(set(round_val_list), key=round_val_list.count)

    ret_dict["real_mode"] = real_mode
    ret_dict["rounded_mode"] = rounded_mode

    return ret_dict

def get_string_tuple_values(str_tuple):
    """
    given tuple string
    "(1, 2, 3, 4, 5, 6)"

    return list of values [1, 2, 3, 4]
    """


    i = 1
    val_list = list()
    curr_val_str = ""
    while(i < len(str_tuple)):
        if(str_tuple[i] == ',' or str_tuple[i] == ')'):
            curr_val_str.strip()

            if(len(curr_val_str) < 1):
                print("Invalid tuple, no value preceeding ,")
                return None
            else:
                #ensure no parenthesis
                if(curr_val_str[0] == '('):
                    curr_val_str = curr_val_str[1:]

                val_list.append(int(curr_val_str))
                curr_val_str = ""
        else:
            curr_val_str += str_tuple[i]

        i += 1

    # print(val_list)
    return val_list


def get_deviations_list(val_list, num):
    """
    Get a list with the deviation of numbers in the
    val list from the num
    """
    deviation_list = list()

    for val in val_list:
        deviation_list.append(abs(num - val))

    return deviation_list

def get_sorted_dict(any_dict):
    return sorted(any_dict.items(), key=lambda kv: kv[1])

def get_sorted_key_list(any_dict):
    """
    input: dictionary with numeric vals
    return: list of keys sorted from least to greatest based on values
    """
    sorted_dict = get_sorted_dict(any_dict)
    sorted_key_list = [i[0] for i in sorted_dict]
    return sorted_key_list


def update_intersect_sets(intersect_set_list, set_list):
    """
    input: intersect_set_list (non_empty), set_list (non_empty)
    saves the intersect of values in the set_list
    interatively
    """
    i = 2
    intersect_index = 0
    temp_set = set()
    prev_temp_set = set()

    while(i < len(set_list)):
        if(intersect_index == 0):
            #save intersect of set_list[0] set_list[1]
            temp_set = intersect_set_list[intersect_index]
            intersect_set_list[intersect_index] = set_list[i].intersection(set_list[i - 1])
        else:
            #save intersection between previous intersect_set and set_list[i]

            #if nothing to intersect clear out the rest of the intersect sect list
            if(len(temp_set) == 0):
                intersect_set_list = intersect_set_list[:intersect_index]
                return
            else:
                prev_temp_set = temp_set
                if(intersect_index < len(intersect_set_list)):
                    temp_set = intersect_set_list[intersect_index]
                    intersect_set_list[intersect_index] = prev_temp_set.intersection(set_list[i])


        intersect_index += 1
        i += 1

def get_intersect_of_set_list(set_list):
    """
    input a list of sets
    read list backwards and get the intersect between the most current draw sets and prev draw sets
    """
    intersect_set_list = list()

    if(len(set_list) > 3):
        for i in range(1, len(set_list) - 1):
            print(set_list[-i])
            if(i == 1):
                intersect_set_list.append(set_list[-i].intersection(set_list[-(i+1)]))
            else:
                #if prev intersection is empty stop
                if(len(intersect_set_list[-1]) == 0):
                    intersect_set_list = intersect_set_list[:-1]
                    break

                intersect_set_list.append(intersect_set_list[-1].intersection(set_list[-(i+1)]))

    return intersect_set_list



def shift_right_list(any_list, shr_in):
    """
    input: set list
    Will move value of index i, to index i + 1
    value at last index removed
    value at last first index = shr_in
    """
    # print("shifting...")
    # print(any_list)
    # print(shr_in)
    shifted_list = list()
    shifted_list.append(shr_in)

    #shifting the list means moving all elements over one index and popping
    #last value
    shifted_list.extend(any_list[:-1])

    any_list = shifted_list

def shift_left_list(any_list, shr_in):
    """
    input: set list
    Will move value of index i+1, to index i
    value at first index removed
    value at last index = shrin
    """
    # print("shifting...")
    # print(any_list)
    # print(shr_in)

    #shifting the list left means moving all elements over one index and popping
    #first value
    #add shr_in value at end of the list
    shifted_list = list()

    #get everything after first
    shifted_list = any_list[1:]
    shifted_list.append(shr_in)



    any_list = shifted_list

def reset_remaining_nums_set():
    from init_functions import init_range_set

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
    if(len(ret_set) < 3):

        if(last_remaining_num_dict is not None):
            #if only one item in set save it
            #get current draw number
            for num in remaining_nums_set:
                # print("Remaining_set_almost empty, current draw #:", current_draw_num, "\n\n")
                last_remaining_num_dict[num] = current_draw_num



        ret_set = reset_remaining_nums_set()
        temp = updated_draws_in_round
        updated_draws_in_round = 0



    else:
        updated_draws_in_round += 1

    ret_dict["remaining_nums_set"] = ret_set
    ret_dict["num_draws_in_round"] = updated_draws_in_round

    return ret_dict




def get_last_n_avg(any_list, n):
    """
    input: any_list, num_elems
    return: avg of the last num_elems of list,
        Or None if len(list) < n
    """
    if(len(any_list) < n):
        # print("Error: List not long enough")
        return None

    return stats.mean(get_last_n_elems(any_list, n))


def get_last_n_elems(any_list, n):
    """
    input: any_list, num_elems
    gets last n elems of any list
    """
    # print(any_list[-n:])
    return any_list[-n:]

def get_last_n_avg_dict(any_list, n_key_list):
    """
    return dict with keys in n_key_list with values as the
    avg of the last_n_elems
    """

    ret_dict = dict()

    for n_key in n_key_list:
        ret_dict[n_key] = get_last_n_avg(any_list, n_key)

    return ret_dict
