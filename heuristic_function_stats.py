import assist_funcs as assist
import init_functions as init
import statistics as stats
from random import randint

last_n_num_correct_dict_list = init.init_dict_list([*range(1, 11)])

def append_to_num_correct_dict_list(num_correct_dict):
    global last_n_num_correct_dict_list

    for n_key in num_correct_dict.keys():
        if(n_key in last_n_num_correct_dict_list.keys()):
            last_n_num_correct_dict_list[n_key].append(num_correct_dict[n_key])

def get_heuristic_stats():
    # print(last_n_num_correct_dict_list)

    for key in last_n_num_correct_dict_list.keys():
        print("N_val:", key, "Avg:", stats.mean(last_n_num_correct_dict_list[key]))
        print("Median:", stats.median(last_n_num_correct_dict_list[key]))
        print("Mode:", max(set(last_n_num_correct_dict_list[key]), key=last_n_num_correct_dict_list[key].count))

        percent_correct = 0
        total_count = len(last_n_num_correct_dict_list[key])

        #get percent of time we get at least on correct
        for num_corr in last_n_num_correct_dict_list[key]:
            if(num_corr >= 1):
                percent_correct += 1

        print("Percent At least one correct:")
        print(percent_correct, total_count, percent_correct / total_count)
        print("\n")





#compare the results of the dict of confidence values and
#compare last 20, 10, 15, etc spot and check percentage of which are selected
def get_last_n_guessed_correct(current_draw_set, sorted_spot_confidence_dict):
    """
    input: current draw set, sorted spot confidence dict
    return percentage of the spots with the highest confidence were used
    in current draw
    """
    global last_n_num_correct_dict_list

    #make dict to hold list of the number correct in the last n values in sorted_spot_confidence_dict
    last_n_num_correct_dict = init.init_dict([*range(1, len(sorted_spot_confidence_dict))])



    #list of spots based on confidence lowest confidence at [0] highest at [-1]
    sorted_spot_confidence_list = [i[0] for i in sorted_spot_confidence_dict]
    # sorted_spot_confidence_list = [randint(1, 80) for i in range(20)]
    print(sorted_spot_confidence_list)

    for n_key in last_n_num_correct_dict.keys():
        #set set of last n values in sorted confidence dict (the one with most confidence)
        # last_n_spot_list = assist.get_last_n_elems(sorted_spot_confidence_list, n_key)
        last_n_spot_list = assist.get_last_n_elems(sorted_spot_confidence_list, n_key)
        # print(last_n_spot_list)
        # print(n_key, last_n_spot_list)
        # print("Current draw set:\n", current_draw_set)
        # print("Last n spot list:\n", last_n_spot_list)
        count = 0

        for spot in last_n_spot_list:
            # print("spot:", spot, "type:", type(spot))
            if(spot in current_draw_set):
                count += 1

        #save count to list of previous num correct counts
        last_n_num_correct_dict[n_key] = count


    print(last_n_num_correct_dict)
    append_to_num_correct_dict_list(last_n_num_correct_dict)
