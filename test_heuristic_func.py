import past_draws_stats as pds
import assist_funcs as assist
import init_functions as init
import heuristic_func as heuristic
import heuristic_function_stats as h_stats

prompt_dict = pds.prompt_for_date()
start_date = prompt_dict["start_date"]
starting_draw_num = pds.date_to_draw_number(start_date)
num_draws_sampled = 0

spot_histogram = init.init_spot_dict()
last_seen_dict = init.init_spot_dict()
prev_means_list = list()
spot_confidence_dict = init.init_spot_dict()
draw_distance_dict = init.init_spot_dict_list()
# print(draw_distance_dict)

# result_dict = pds.get_most_recent_draw()
sorted_spot_confidence_dict = None
winning_sets_list = list()

while(num_draws_sampled < prompt_dict["num_days_to_sample"] * 300):
    print(num_draws_sampled, starting_draw_num)
    result_dict = pds.get_results_from_draw_num(starting_draw_num, draw_distance_dict=draw_distance_dict, last_seen_dict=last_seen_dict, spot_histogram=spot_histogram)
    winning_spot_list = result_dict["spot_list"]
    winning_sets_list.append(winning_spot_list)
    prev_means_list.append(result_dict["mean"])
    print(winning_spot_list)


    # print(draw_distance_dict)

    if(num_draws_sampled > 50):
        if(sorted_spot_confidence_dict is not None):
            h_stats.get_last_n_guessed_correct(winning_spot_list, sorted_spot_confidence_dict)

        #least confidnce [0] most confidence [-1]
        sorted_spot_confidence_dict = heuristic.get_confidence_values(spot_confidence_dict, current_draw_num=starting_draw_num, spot_histogram=spot_histogram,
            last_seen_dict=last_seen_dict, prev_means_list=prev_means_list, draw_distance_dict=draw_distance_dict, winning_sets_list=winning_sets_list)

    num_draws_sampled += 1
    starting_draw_num += 1


print(h_stats.get_heuristic_stats())
