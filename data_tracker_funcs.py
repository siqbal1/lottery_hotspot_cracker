import drawing_set_stats as dss
import past_draws_stats as pds
import assist_funcs as assist

def update_last_remaining_draw_distance(current_draw_num, num):
    """
    update list of last remaining numbers draw distances
    """

    #save to list
    if(num in dss.last_remaining_num_dict_list.keys()):
        #pop num from last_remaining_num_dict, value holds draw num of draw num when last remaining dict was almost empty
        last_remaining_draw_distance = abs(current_draw_num - dss.last_remaining_num_dict[num])
        val = dss.last_remaining_num_dict.pop(num)

        # print("Last remaining num dict start draw num:", val)
        # print("Last remaining num", num, "distance: ", last_remaining_draw_distance)

        dss.last_remaining_num_dict_list[num].append(last_remaining_draw_distance)

    #save last remaining num for round legnth
    if(len(dss.last_remaining_num_dict) == 1):
        #convert to list first to enable list indexing
        dss.last_remaining_num = list(dss.last_remaining_num_dict.keys())[0]
        # print("Last remaining num:", dss.last_remaining_num,
        #     " current distance", abs(dss.last_remaining_num_dict[dss.last_remaining_num] - current_draw_num))

def update_last_n_avg_draw_distances(last_n_val, num, draw_distance_dict, last_n_avg_distance_dict_list=None,
    last_n_avg_distance_dict=None):
    """
    update avgs of last_n_avg_distance_dict by getting the avg of
    prev2 draw distances
    ...
    prev_last_n_val draw distances
    """

    last_n_avg_key = 2

    # print(draw_distance_dict)
    # print("\n\n\n\n", last_n_avg_distance_dict)

    while(last_n_avg_key <= last_n_val  and last_n_avg_key <= len(draw_distance_dict[num])):
        distance_avg = assist.get_last_n_avg(draw_distance_dict[num], last_n_avg_key)

        if(distance_avg is not None):
            #for stats calculations
            if(last_n_avg_distance_dict_list is not None):
                append_to_last_n_avg_dict_list(num, last_n_avg_key, distance_avg, last_n_avg_distance_dict_list)

            #for current drawings
            if(last_n_avg_distance_dict is not None):
                last_n_avg_distance_dict[num][last_n_avg_key] = distance_avg

        last_n_avg_key += 1

# last_seen_dict, draw_distance_dict, avg_draw_distance_dict,
#     last_n_avg_distance_dict, current_draw_num,
def increment_draw_distance_sums(current_draw_num, num, last_seen_dict, draw_distance_dict, avg_draw_distance_dict=None,
    last_n_avg_distance_dict_list=None, last_n_avg_distance_dict=None):
    """
    Increases sum of the distance between draws in which the number
    was selected as a winner

    Input: stats_dict, num_spot
    """
    # print(last_seen_dict)

    # print(last_n_avg_distance_dict)

    # print("Draw Distance Sums")
    # print(current_draw_num)
    # print(last_seen_dict[num])

    #find diff in draw nums
    draw_distance = abs(current_draw_num - last_seen_dict[num])

    if(avg_draw_distance_dict is not None):
        avg_draw_distance_dict[num] += draw_distance

    last_seen_dict[num] = current_draw_num

    # print("Draw Distance " + str(num) + ": " + str(draw_distance))

    draw_distance_dict[num].append(draw_distance)

    #if seen one of the last remaining set of current draw
    # update_last_remaining_draw_distance(current_draw_num, num)

    #get the avg of last n elements for winning num, append to dict list
    update_last_n_avg_draw_distances(pds.last_n, num, draw_distance_dict, last_n_avg_distance_dict_list,
        last_n_avg_distance_dict)

def increment_mod_hist(mod_histogram, num):
    """
    Increment values in mod_hist dictionary
    Input: number
    """
    if(num % 2 == 0):
        mod_histogram["even"] += 1
    else:
        mod_histogram["odd"] += 1

    if(num % 3 == 0):
        mod_histogram[3] += 1
    elif(num % 5 == 0):
        mod_histogram[5] += 1

    if(num % 10 == 0):
        mod_histogram[10] += 1

    #check if there is a higher chance of ending in a specific number
    ending_num = num % 10
    end_key = "end_in_" + str(ending_num)
    mod_histogram[end_key] += 1


def increment_range_hist(range_histogram, num):
    if(num >= 1 and num <= 10):
        range_histogram["1-10"] += 1
    elif(num >= 11 and num <= 20):
        range_histogram["11-20"] += 1
    elif(num >= 21 and num <= 30):
        range_histogram["21-30"] += 1
    elif(num >= 31 and num <= 40):
        range_histogram["31-40"] += 1
    elif(num >= 41 and num <= 50):
        range_histogram["41-50"] += 1
    elif(num >= 51 and num <= 60):
        range_histogram["51-60"] += 1
    elif(num >= 61 and num <= 70):
        range_histogram["61-70"] += 1
    else:
        #(num >= 71 and num <= 80):
        range_histogram["71-80"] += 1

def increment_spot_hist(spot_histogram, num):
    if num not in spot_histogram.keys():
        spot_histogram[num] = 1
    else:
        spot_histogram[num] += 1

def append_to_last_n_avg_dict_list(spot_num, last_n_avg_key, last_n_avg, last_n_avg_distance_dict):
    # print(spot_num, "last", last_n_avg_key, "n avg:", last_n_avg)
    last_n_avg_distance_dict[spot_num][last_n_avg_key].append(last_n_avg)
