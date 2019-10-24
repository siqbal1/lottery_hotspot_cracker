import json
import past_draws_stats as pds
from datetime import date
from datetime import timedelta
import file_reading_funcs as read
import init_functions as init
# prompt_dict = pds.prompt_for_date()
# starting_date = date(prompt_dict["year"], prompt_dict["month"], prompt_dict[["day"]])
# sample_num = prompt_dict["sample_num"]


try:
    start_date = date(2019, 10, 11)
    f_name = "milestone_histogram_stats/" + str(start_date) + "_milestone_dict.json"
    milestone_dict = read.read_dict_from_file(f_name)

    #keep list of the difference of draws between when spots reach the next expect value compared
    #to the milestone
    draws_till_next_expected = init.init_dict_list([str(x) for x in range(1, 81)])
    #save the differences in number of draw required for each milestone
    prev_milestone_lambda_count = dict()
    end_loop = False

    for milestone_key in milestone_dict:


        lambda_count_dict =  milestone_dict[milestone_key]["lambda_draw_count"]
        lambda_val = milestone_dict[milestone_key]["lambda"]

        for spot_key in lambda_count_dict.keys():
            if(spot_key in prev_milestone_lambda_count.keys()):
                lambda_count = int(lambda_count_dict[spot_key])
                prev_lambda_count = int(prev_milestone_lambda_count[spot_key])

                #get difference between the milestone draws
                if(lambda_count == 0):
                    end_loop = True
                    break


                draw_diff = abs(lambda_count - prev_lambda_count)
                print("Prev Expected:", prev_milestone_lambda_count["lambda"], "Expected count:", milestone_dict[milestone_key]["lambda"])
                print("Spot:", spot_key, "draw diff", lambda_count, prev_lambda_count, "=", draw_diff)
                draws_till_next_expected[spot_key].append(draw_diff)

            prev_milestone_lambda_count[spot_key] = lambda_count_dict[spot_key]

        prev_milestone_lambda_count["lambda"] = lambda_val


        if(end_loop):
            end_loop = False
            break


finally:
    print(draws_till_next_expected)
