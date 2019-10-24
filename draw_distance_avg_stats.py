import json
import init_functions as init
import statistics as stats
import assist_funcs as assist
import drawing_set_stats as dss
import random as random
import parse_last_n_avg_stats as last_n_stats

#get any list of spots and check last n_avg of random list sample
sample_num = input("Enter sample file #: ")


file_name = "s" + sample_num + "_stats/draw_distances_sample_" + sample_num + ".json"

with open(file_name, "r") as json_file:

    stats_dict_list = init.init_dict_list(init.get_last_n_avg_key_list(15))
    draw_distance_dict = json.load(json_file)

    spot_key = input("Enter spot # to sample: ")

    while(spot_key != "0"):

        draw_distance_list = draw_distance_dict[spot_key]

        #for each n last elements get stats (avg, min, max, etc.)
        for n in range(2, 16):
            print("\n\nSpot key =", spot_key, "last", n, " stats:")

            last_n_list = assist.get_last_n_elems(draw_distance_list, n)
            stats_dict = last_n_stats.get_list_stats(last_n_list)
            dss.print_dict(stats_dict)

            stats_dict_list[n].append(stats_dict)

        distance_histogram = dict()

        #for each spot find a count for the draw distances
        #find medium mode, std dev of draw distances
        for draw_distance in draw_distance_list:
            if(draw_distance not in distance_histogram.keys()):
                distance_histogram[draw_distance] = 1
            else:
                distance_histogram[draw_distance] += 1

        distance_mean = stats.mean(draw_distance_list)
        distance_std_dev = stats.stdev(draw_distance_list, xbar=distance_mean)
        distance_median = stats.median(draw_distance_list)
        distance_mode = max(set(draw_distance_list), key=draw_distance_list.count)

        print("Mean of draw distances:", distance_mean)
        print("Std dev of draw distances:", distance_std_dev)
        print("Median of draw distances:", distance_median)
        print("Mode of draw distances:", distance_mode)
        print("Draw distance histogram:\n", assist.get_sorted_dict(distance_histogram))


        spot_key = input("Enter spot # to sample: ")


    json_file.close()

#hold list of avgs and std_dev for each nums last_n_avg_draw distance stats
full_stats_dict_list = init.init_dict_dict_list(init.get_last_n_avg_key_list(15), ["avg", "std_dev"])

#get list of stats from current session
for n_val_key in stats_dict_list:
    #loop through each stat dict in list
    for stat_dict in stats_dict_list[n_val_key]:
        full_stats_dict_list[n_val_key]["avg"].append(stat_dict["avg"])
        full_stats_dict_list[n_val_key]["std_dev"].append(stat_dict["std_dev"])


dss.print_dict(full_stats_dict_list)
