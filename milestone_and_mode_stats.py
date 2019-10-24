from datetime import date
from datetime import timedelta
import file_reading_funcs as read
import file_writing_funcs as write
import assist_funcs as assist
import init_functions as init
import json

# try:
#     spot_index_dict = init.init_spot_dict_list()
#     spot_count_dict_list = init.init_spot_dict_list()
#
#     start_date = date(2019, 9, 1)
#
#     while(1):
#
#         f_name = "milestone_histogram_stats/" + str(start_date) + "_ordered_histogram.txt"
#
#         print(f_name)
#         ordered_tuple_list = read.read_list_from_file(f_name)
#         #convert strings to list values
#         ordered_tuple_list = [assist.get_string_tuple_values(tuple) for tuple in ordered_tuple_list]
#
#
#         for index, tuple in enumerate(ordered_tuple_list):
#             spot = tuple[0]
#             count = tuple[1]
#
#             spot_index_dict[spot].append(index)
#             spot_count_dict_list[spot].append(count)
#
#         print(spot_index_dict)
#         print(spot_count_dict_list)
#
#         start_date += timedelta(days=1)
#
# except TypeError:
#     print("Spot Index Dict:")
#     print(spot_index_dict, "\n\n")
#
#     print("Spot Count Lists:")
#     print(spot_count_dict_list, "\n\n")
#
#     great_app_count = 0
#     less_app_count = 0
#     not_great_app_count = 0
#     not_less_app_count = 0
#     total_count = 0
#     great_count = 0
#     less_count = 0
#     not_count = 0
#
#     for spot_index_list in spot_index_dict.values():
#
#
#         for i, index_val in enumerate(spot_index_list):
#
#             if(index_val < 3):
#                 less_count += 1
#                 total_count += 1
#                 if(i + 1 < len(spot_index_list)):
#                     if(spot_index_list[i+1] < 40):
#                         less_app_count += 1
#                         print(index_val, spot_index_list[i+1], less_app_count)
#                     else:
#                         print(index_val, spot_index_list[i+1], " not less app count")
#                         not_less_app_count += 1
#                         not_count +=1
#
#             if(index_val > 76):
#                 great_count += 1
#                 total_count += 1
#                 if(i + 1 < len(spot_index_list)):
#                     if(spot_index_list[i+1] > 40 ):
#                         great_app_count += 1
#
#                         print(index_val, spot_index_list[i+1], great_app_count)
#                     else:
#                         print(index_val, spot_index_list[i+1], " not great app count")
#                         not_great_app_count += 1
#                         not_count += 1
#
#
#
#     print("\n", less_app_count, less_count, "\n", great_count, great_app_count, "\n", total_count)
#     print(not_less_app_count, not_great_app_count, "\n", not_count)

milestone_json_file_name = "milestone_histogram_stats/2019-10-12_milestone_dict.json"

milestone_stat_dict = dict()

with open(milestone_json_file_name) as json_file:
    milestone_dict = json.load(json_file)
    # print(milestone_dict)

    for milestone_key in milestone_dict.keys():
        lambda_draw_count_list = milestone_dict[milestone_key]["lambda_draw_count"].values()
        lambda_draw_count_list = [int(x) for x in lambda_draw_count_list]

        print(lambda_draw_count_list)

        milestone_stat_dict[milestone_key] = dict()

        milestone_stat_dict[milestone_key]["lambda"] = milestone_dict[milestone_key]["lambda"]
        milestone_stat_dict[milestone_key]["lambda_draw_count_stats"] = assist.get_list_stats(lambda_draw_count_list)

    # print(milestone_stat_dict)

    write.write_dict_to_file(milestone_stat_dict, "milestone_stats.json")
