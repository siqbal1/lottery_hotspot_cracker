import init_functions as init
import json
from parse_last_n_avg_stats import get_list_stats
import assist_funcs as assist

# def test_consecutive_winners():


sample_num = input("Enter sample file #: ")

file_name = "s" + sample_num + "_stats/draw_distances_sample_" + sample_num + ".json"

with open(file_name, "r") as json_file:
    draw_distance_dict_list = json.load(json_file)

    starting_large_dist = 1


    spot_key = "1"

    while(spot_key != "0"):
        draw_distance_list = draw_distance_dict_list[spot_key]


        #if we find a one, means consecutive draw winner, get prev draws
        # print("Spot:", spot_key)
        # for i in range(len(draw_distance_list)):
        #     if(draw_distance_list[i] == 1):
        #         print(assist.get_last_n_elems(draw_distance_list[:i], 10))
        #         print(assist.get_last_n_avg(draw_distance_list[:i], 10))
        after_one_hist = init.init_dict([*range(1, 15)])

        for index,dist in enumerate(draw_distance_list):
            # print(index, dist)
            if(dist == 1):
                if(index -  1 >= 0 and index + 1 < len(draw_distance_list)):
                    print(draw_distance_list[index -  1], dist, draw_distance_list[index + 1])

                    if(draw_distance_list[index + 1] in after_one_hist.keys()):
                        after_one_hist[draw_distance_list[index + 1]] += 1
            if(dist >= 8):
                if(index -  1 >= 0 and index + 1 < len(draw_distance_list)):
                    print(draw_distance_list[index -  1], dist, draw_distance_list[index + 1])






        print(after_one_hist)



        spot_key = input("Next spot key:")

        #check for each

    #save values of
    # proportion_dict_list = init.init_dict_list([*range(1, 30)])
    # dist_count_dict_list = init.init_dict_list([*range(1, 30)])
    #
    #
    # while(spot_key != "0"):
    #     #test after a large number, >= 8, histogram of numbers
    #     # spot_key = input("Enter spot # to sample: ")
    #     draw_distance_list = draw_distance_dict_list[spot_key]
    #     next_dist_histogram= init.init_dict([*range(1, 30)])
    #
    #     for dist in draw_distance_list:
    #         if(dist >= starting_large_dist):
    #             if(dist not in next_dist_histogram):
    #                 next_dist_histogram[dist] = 1
    #             else:
    #                 next_dist_histogram[dist] += 1
    #
    #
    #     print(next_dist_histogram)
    #
    #     proportion_dict = dict()
    #
    #     for key in next_dist_histogram.keys():
    #         proportion = float(next_dist_histogram[key] / len(draw_distance_dict_list[spot_key]))
    #         proportion_dict[key] = proportion
    #
    #         if(key in proportion_dict_list):
    #             proportion_dict_list[key].append(proportion)
    #             dist_count_dict_list[key].append(next_dist_histogram[key])
    #
    #
    #     print(proportion_dict)
    #
    #     spot_key = int(spot_key)
    #     spot_key += 1
    #     spot_key = str(spot_key)
    #
    #     if(spot_key == "81"):
    #         spot_key = "0"

        #save values to dict key list

#get stats on both proportion and dist count lists
# print(proportion_dict_list)
# print(dist_count_dict_list)
#
# for dist_key in proportion_dict_list.keys():
#     #get stats on list values
#     if(dist_key < 10):
#         print(dist_key, "\n", get_list_stats(proportion_dict_list[dist_key]))
#
# print("\n\n")
#
# for dist_key in dist_count_dict_list.keys():
#     if(dist_key < 10):
#         print(dist_key, "\n", get_list_stats(dist_count_dict_list[dist_key]))
