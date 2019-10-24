"""
Get stats on the draw distances for getting n wins
ex: the avg, std dev, etc for the draw distances it takes for a spot to get 2 spot wins
"""

import file_reading_funcs as read
import init_functions as init
import assist_funcs as assist
import file_writing_funcs as write

results_dict = dict()

try:
    while(1):
        sample_num = input("Sample num:")
        file_name = "s" + sample_num + "_inter_draw_dist.json"
        n_wins_dict = read.read_dict_from_file(file_name)

        for n_wins_key, draw_dist_list in n_wins_dict.items():
            list_stats = assist.get_list_stats(draw_dist_list)
            list_stats["list_size"] = len(draw_dist_list)

            for stat_key, stat_val in list_stats.items():
                if(stat_key not in results_dict.keys()):
                    results_dict[stat_key] = dict()

                if(n_wins_key not in results_dict[stat_key].keys()):
                    results_dict[stat_key][n_wins_key] = [stat_val]
                else:
                    results_dict[stat_key][n_wins_key].append(stat_val)

            print(n_wins_key, "wins stats:")
            print(list_stats)


finally:
    for stat_key in results_dict.keys():
        print(stat_key, results_dict[stat_key])

    write.write_dict_to_file(results_dict, "inter_draw_dist_stats.json")
