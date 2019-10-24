import past_draws_stats as pds
import assist_funcs as assist
import init_functions as init
import file_reading_funcs as read
import statistics as stats

sample_num = input("Sample number:")
f_name = "s" + str(sample_num) + "_stats/sample_means_list_sample_2" + ".txt"

while(1):
    #test for each sample mean
    avg_list = read.read_mean_list(f_name)

    print(avg_list)
    avg_stats_dict = assist.get_list_stats(avg_list)
    print(avg_stats_dict)

    total_lts = 0
    matching_lts = 0

    total_stl = 0
    matching_stl = 0

    for index, avg in enumerate(avg_list):
        if(index > 1):
            if(avg > avg_stats_dict["avg"] + avg_stats_dict["std_dev"] and not avg_list[index - 1] < avg_stats_dict["avg"] - 3):
                if(index + 1 < len(avg_list)):
                    if(avg_list[index+1] < 40):
                        print("Matching")
                        matching_lts += 1
                    else:
                        print("Against")

                    total_lts += 1
                    try:
                        print(avg_list[index - 3], avg_list[index - 2], avg_list[index - 1], avg, avg_list[index+1])
                    except Exception as e:
                        continue

    for index, avg in enumerate(avg_list):
        if(index >= 1):
            if(avg < avg_stats_dict["avg"] - avg_stats_dict["std_dev"] and not avg_list[index - 1] < avg_stats_dict["avg"] + 3):
                if(index + 1 < len(avg_list) ):
                    if(avg_list[index+1] > 40):
                        print("Matching")
                        matching_stl += 1
                    else:
                        print("Against")

                    total_stl += 1
                    try:
                        print(avg_list[index - 3], avg_list[index - 2], avg_list[index - 1], avg, avg_list[index+1])
                    except Exception as e:
                        continue

    print(matching_lts, total_lts, float(matching_lts / total_lts))
    print(matching_stl, total_stl, float(matching_stl / total_stl))

    sample_num = input("Next sample number:")
    f_name = "s" + str(sample_num) + "_stats/sample_means_list_sample_" + str(2) + ".txt"
