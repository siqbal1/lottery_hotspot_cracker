import assist_funcs as assist
import init_functions as init
import file_reading_funcs as read
import file_writing_funcs as write

matching_dict = dict()

try:
    while(1):
        sample_num = input("Enter Sample Num:")
        f_name =  "s" + sample_num + "_stats/draw_distances_sample_" + sample_num + ".json"

        draw_dist_list_dict = read.read_dict_from_file(f_name)


        for spot_key in draw_dist_list_dict.keys():
            draw_dist_list = draw_dist_list_dict[spot_key]

            total_count = 0
            matching_count = 0

            for index, dist in enumerate(draw_dist_list):
                dist = int(dist)
                if(index > 5):
                    # check how often spots with low winning avgs are picked
                    # draw_dist_list[index - 4] <= 2 and draw_dist_list[index - 3] <= 2 and draw_dist_list[index - 2] <= 2 and draw_dist_list[index - 1] <= 2
                    if(draw_dist_list[index - 4] <= 2 and draw_dist_list[index - 3] <= 2 and draw_dist_list[index - 2] <= 2 and draw_dist_list[index - 1] <= 2):
                        if(dist <= 2):
                            print("Matching")
                            matching_count += 1
                        else:
                            print("Detracting")

                        total_count += 1

                        print(draw_dist_list[index - 2], draw_dist_list[index - 1], dist)

                    # test percent of time if long draw distance what following draw distance is going to be
                    # if(draw_dist_list[index - 1] >= 8):
                    #     if(dist <= 3):
                    #         print("Matching")
                    #         matching_count += 1
                    #
                    #     else:
                    #         print("Detracting")
                    #
                    #     print(draw_dist_list[index - 1], dist)
                    #
                    #     total_count += 1


            if(total_count != 0):
                matching_dict[sample_num] = {"matching" : matching_count,
                    "total" : total_count,
                    "percent" : float(matching_count / total_count)
                    }

                print(matching_dict[sample_num])
finally:
    write.write_dict_to_file(matching_dict, "quad_low_draw_dist.json")
