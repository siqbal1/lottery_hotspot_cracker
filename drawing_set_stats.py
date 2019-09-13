from statistics import mean
from statistics import stdev
from statistics import variance

#set for all numbers in hotspot range
range_set = set()
#set to keep track of the numbers that have not been played
#in current round
#when all numbers have been played
#increment count and reset the remaining_nums_set
#find avg num draws that it takes to use all nums at least once
#find percentage of current draw that comes from
#the numbers that havent been played during this round
remaining_nums_set = set()

for i in range(1, 81):
    range_set.add(i)
    remaining_nums_set.add(i)

#keep track of amount of draws needed to complete one round
#one round is complete when the remaining_nums_set becomes empty
#and is reset
num_draws_in_round = 0

def reset_remaining_nums_set():
    global remaining_nums_set

    for i in range(1, 81):
        remaining_nums_set.add(i)

def update_remaining_nums_set(current_draw_set):
    """
    input: current draw set
    return: if remaining_nums_set is empty, return num draws
    that it took for all nums in range to be winning nums
    """
    global remaining_nums_set
    global num_draws_in_round

    remaining_nums_set = remaining_nums_set - current_draw_set
    print(remaining_nums_set)

    #if not eneough data points
    #reset anyways to not skew stats
    if(len(remaining_nums_set) < 5):
        reset_remaining_nums_set()
        temp = num_draws_in_round
        num_draws_in_round = 0
        return temp
    else:
        num_draws_in_round += 1
        return 0

def print_dict(any_dict):
    for key, value in any_dict.items():
        print(key, value)

def get_set_stats(current_draw_set, prev_draw_set, prev2_draw_set, prev3_draw_set, prev4_draw_set):
    """
    Input: current and last 4 sets
    Output: dict with set statistics

    ret_dict {
        percent_prev_losers_selected
        percent_prev2_losers_selected
        percent_prev3_losers_selected
        percent_prev4_losers_selected

        percent_prev_winners_selected
        percent_prev2_winners_selected
        percent_prev3_winners_selected
        percent_prev4_winners_selected
    }
    """
    global remaining_nums_set

    set_stats_dict = {}

    #set of nums for all losers for the draws
    prev_losers_selected = get_losers_for_draw_set(prev_draw_set)
    prev2_losers_selected = get_losers_for_draw_set(prev2_draw_set)
    prev3_losers_selected = get_losers_for_draw_set(prev3_draw_set)
    prev4_losers_selected = get_losers_for_draw_set(prev4_draw_set)

    #set of numbers for intersection of losers
    #get the percentage of common losing numbers across multiple draws
    #compare with current draw to get a percentage
    intersect_prev2_losers = prev_losers_selected.intersection(prev2_losers_selected)
    intersect_prev3_losers = intersect_prev2_losers.intersection(prev3_losers_selected)
    intersect_prev4_losers = intersect_prev3_losers.intersection(prev4_losers_selected)

    #highest percent of nums come from prev2 losers and remaining nums
    #find percentage of the intersect that appear
    intersect_prev2_losers_remaining_nums = intersect_prev2_losers.intersection(remaining_nums_set)

    print("Intersect Prev 2 losers")
    print(intersect_prev2_losers)
    print("Intersect Prev 3 losers")
    print(intersect_prev3_losers)
    print("Intersect Prev 4 losers")
    print(intersect_prev4_losers)
    print("Intersect Prev 2 losers and remaining nums")
    print(intersect_prev2_losers_remaining_nums)

    #percent common between losers of prev sets and winner of current set
    set_stats_dict["percent_prev_losers_selected"] = get_percent_common_s2(current_draw_set, prev_losers_selected)
    set_stats_dict["percent_prev2_losers_selected"] = get_percent_common_s2(current_draw_set, prev2_losers_selected)
    set_stats_dict["percent_prev3_losers_selected"] = get_percent_common_s2(current_draw_set, prev3_losers_selected)
    set_stats_dict["percent_prev4_losers_selected"] = get_percent_common_s2(current_draw_set, prev4_losers_selected)


    #percent of how much of the winning numbers came from previous loser sets
    #percent composition of prev losers to curr winners
    set_stats_dict["percent_selected_from_prev_losers"] = get_percent_common_s1(current_draw_set, prev_losers_selected)
    set_stats_dict["percent_selected_from_prev2_losers"] = get_percent_common_s1(current_draw_set, prev2_losers_selected)
    set_stats_dict["percent_selected_from_prev3_losers"] = get_percent_common_s1(current_draw_set, prev3_losers_selected)
    set_stats_dict["percent_selected_from_prev4_losers"] = get_percent_common_s1(current_draw_set, prev4_losers_selected)

    #percent common between winners of prev sets and winners of current set
    set_stats_dict["percent_prev_winners_selected"] = get_percent_common_s2(current_draw_set, prev_draw_set)
    set_stats_dict["percent_prev2_winners_selected"] = get_percent_common_s2(current_draw_set, prev2_draw_set)
    set_stats_dict["percent_prev3_winners_selected"] = get_percent_common_s2(current_draw_set, prev3_draw_set)
    set_stats_dict["percent_prev4_winners_selected"] = get_percent_common_s2(current_draw_set, prev4_draw_set)

    #percent of how much of the winning numbers came from previous winning sets
    #percent composition of prev winners to curr winners
    set_stats_dict["percent_selected_from_prev_winners"] = get_percent_common_s1(current_draw_set, prev_draw_set)
    set_stats_dict["percent_selected_from_prev2_winners"] = get_percent_common_s1(current_draw_set, prev2_draw_set)
    set_stats_dict["percent_selected_from_prev3_winners"] = get_percent_common_s1(current_draw_set, prev3_draw_set)
    set_stats_dict["percent_selected_from_prev4_winners"] = get_percent_common_s1(current_draw_set, prev4_draw_set)

    #percent of how many of the previous common losers (among previous draws) were
    #selected as winners in the current draw
    set_stats_dict["percent_intersect_prev2_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev2_losers)
    set_stats_dict["percent_intersect_prev3_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev3_losers)
    set_stats_dict["percent_intersect_prev4_losers_selected"] = get_percent_common_s2(current_draw_set, intersect_prev4_losers)

    #percent composition of the current draw winning numbers from intersection of prev draw losers
    set_stats_dict["percent_selected_from_intersect_prev2_losers"] = get_percent_common_s1(current_draw_set, intersect_prev2_losers)
    set_stats_dict["percent_selected_from_intersect_prev3_losers"] = get_percent_common_s1(current_draw_set, intersect_prev3_losers)
    set_stats_dict["percent_selected_from_intersect_prev4_losers"] = get_percent_common_s1(current_draw_set, intersect_prev4_losers)

    #get percent of remaining nums selected as winners in current draw
    set_stats_dict["percent_remaining_nums_selected"] = get_percent_common_s2(current_draw_set, remaining_nums_set)
    #percent composition of current winning nums from the remaining losing nums set
    set_stats_dict["percent_selected_from_remaining_nums"] = get_percent_common_s1(current_draw_set, remaining_nums_set)

    #percent of the intersect of the prev2 losers and remaining nums that are selected as winners
    set_stats_dict["percent_intersect_prev2_losers_remaining_nums_selected"] = get_percent_common_s2(current_draw_set, intersect_prev2_losers_remaining_nums)
    #percent composition of current winning numbers with the intersect of prev 2 losers and remaining nums
    set_stats_dict["percent_selected_from_intersect_prev2_losers_remaining_nums"] = get_percent_common_s1(current_draw_set, intersect_prev2_losers_remaining_nums)

    #update remaining nums set to get rid of most recent winning nums
    #if remaining_nums_set empty return num draws that it took
    round_len = update_remaining_nums_set(current_draw_set)
    if(round_len > 0):
        set_stats_dict["num_draws_in_round"] = round_len

    print_dict(set_stats_dict)
    return set_stats_dict


def get_losers_for_draw_set(draw_set):
    """
    Input: draw_set
    output: set of losing numbers for that draw
    """
    return range_set - draw_set

def get_percent_common_s1(s1, s2):
    """
    Input: set1, set2
    output: percent of composition of s1 from s2
    """
    #s2 = prev_set
    #s1 = curr_set
    common_set = s1.intersection(s2)

    #percent composition of s1 from s2
    return len(common_set) / float(len(s1))


def get_percent_common_s2(s1, s2):
    """
    Input: set1, set2
    output: percent of nums in current_set that exists in the other set s2
    """

    #s2 = prev_set
    #s1 = curr_set
    common_set = s1.intersection(s2)

    #percent of s1 that comes from s2
    return len(common_set) / float(len(s2))

def parse_ppls_set_stats(set_stats_dict, ppls_list, pp2ls_list, pp3ls_list, pp4ls_list):
    #percent previous losers selected
    ppls_list.append(set_stats_dict["percent_prev_losers_selected"])
    pp2ls_list.append(set_stats_dict["percent_prev2_losers_selected"])
    pp3ls_list.append(set_stats_dict["percent_prev3_losers_selected"])
    pp4ls_list.append(set_stats_dict["percent_prev4_losers_selected"])

def parse_ppws_set_stats(set_stats_dict, ppws_list, pp2ws_list, pp3ws_list, pp4ws_list):
    #percent previous winners selected
    ppws_list.append(set_stats_dict["percent_prev_winners_selected"])
    pp2ws_list.append(set_stats_dict["percent_prev2_winners_selected"])
    pp3ws_list.append(set_stats_dict["percent_prev3_winners_selected"])
    pp4ws_list.append(set_stats_dict["percent_prev4_winners_selected"])

def parse_psfpl_set_stats(set_stats_dict, psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list):
    #percent selected from previous losers
    psfpl_list.append(set_stats_dict["percent_selected_from_prev_losers"])
    psfp2l_list.append(set_stats_dict["percent_selected_from_prev2_losers"])
    psfp3l_list.append(set_stats_dict["percent_selected_from_prev3_losers"])
    psfp4l_list.append(set_stats_dict["percent_selected_from_prev4_losers"])

def parse_psfpw_set_stats(set_stats_dict, psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list):
    #percent selected from previous losers
    psfpw_list.append(set_stats_dict["percent_selected_from_prev_winners"])
    psfp2w_list.append(set_stats_dict["percent_selected_from_prev2_winners"])
    psfp3w_list.append(set_stats_dict["percent_selected_from_prev3_winners"])
    psfp4w_list.append(set_stats_dict["percent_selected_from_prev4_winners"])

def parse_pipls_set_stats(set_stats_dict, pip2ls_list, pip3ls_list, pip4ls_list):
    pip2ls_list.append(set_stats_dict["percent_intersect_prev2_losers_selected"])
    pip3ls_list.append(set_stats_dict["percent_intersect_prev3_losers_selected"])
    pip4ls_list.append(set_stats_dict["percent_intersect_prev4_losers_selected"])


def parse_psfip_set_stats(set_stats_dict, psfip2_list, psfip3_list, psfip4_list):
    #psfip -> percent_selected_from_intersect_prev_losers
    psfip2_list.append(set_stats_dict["percent_selected_from_intersect_prev2_losers"])
    psfip3_list.append(set_stats_dict["percent_selected_from_intersect_prev3_losers"])
    psfip4_list.append(set_stats_dict["percent_selected_from_intersect_prev4_losers"])

def parse_remaining_nums_set_stats(set_stats_dict, prns_list, psfrn_list, draws_per_round_list):
    prns_list.append(set_stats_dict["percent_remaining_nums_selected"])
    psfrn_list.append(set_stats_dict["percent_selected_from_remaining_nums"])

    if("num_draws_in_round" in set_stats_dict.keys()):
        draws_per_round_list.append(set_stats_dict["num_draws_in_round"])

def parse_intersect_remaining_num_set_stats(set_stats_dict, pip2lrns_list, psfip2lrn_list):
    pip2lrns_list.append(set_stats_dict["percent_intersect_prev2_losers_remaining_nums_selected"])
    psfip2lrn_list.append(set_stats_dict["percent_selected_from_intersect_prev2_losers_remaining_nums"])

def get_ppls_stats(ppls_list, pp2ls_list, pp3ls_list, pp4ls_list):
    result_dict = {}

    result_dict["avg_ppls"] = mean(ppls_list)
    result_dict["avg_pp2ls"] = mean(pp2ls_list)
    result_dict["avg_pp3ls"] = mean(pp3ls_list)
    result_dict["avg_pp4ls"] = mean(pp4ls_list)

    result_dict["std_dev_ppls"] = stdev(ppls_list, xbar=result_dict["avg_ppls"])
    result_dict["std_dev_pp2ls"] = stdev(pp2ls_list, xbar=result_dict["avg_pp2ls"])
    result_dict["std_dev_pp3ls"] = stdev(pp3ls_list, xbar=result_dict["avg_pp3ls"])
    result_dict["std_dev_pp4ls"] = stdev(pp4ls_list, xbar=result_dict["avg_pp4ls"])

    result_dict["variance_ppls"] = variance(ppls_list, xbar=result_dict["avg_ppls"])
    result_dict["variance_pp2ls"] = variance(pp2ls_list, xbar=result_dict["avg_pp2ls"])
    result_dict["variance_pp3ls"] = variance(pp3ls_list, xbar=result_dict["avg_pp3ls"])
    result_dict["variance_pp4ls"] = variance(pp4ls_list, xbar=result_dict["avg_pp4ls"])

    return result_dict

def get_ppws_stats(ppws_list, pp2ws_list, pp3ws_list, pp4ws_list):
    result_dict = {}

    result_dict["avg_ppws"] = mean(ppws_list)
    result_dict["avg_pp2ws"] = mean(pp2ws_list)
    result_dict["avg_pp3ws"] = mean(pp3ws_list)
    result_dict["avg_pp4ws"] = mean(pp4ws_list)

    result_dict["std_dev_ppws"] = stdev(ppws_list, xbar=result_dict["avg_ppws"])
    result_dict["std_dev_pp2ws"] = stdev(pp2ws_list, xbar=result_dict["avg_pp2ws"])
    result_dict["std_dev_pp3ws"] = stdev(pp3ws_list, xbar=result_dict["avg_pp3ws"])
    result_dict["std_dev_pp4ws"] = stdev(pp4ws_list, xbar=result_dict["avg_pp4ws"])

    result_dict["variance_ppws"] = variance(ppws_list, xbar=result_dict["avg_ppws"])
    result_dict["variance_pp2ws"] = variance(pp2ws_list, xbar=result_dict["avg_pp2ws"])
    result_dict["variance_pp3ws"] = variance(pp3ws_list, xbar=result_dict["avg_pp3ws"])
    result_dict["variance_pp4ws"] = variance(pp4ws_list, xbar=result_dict["avg_pp4ws"])

    return result_dict

def get_psfpl_stats(psfpl_list, psfp2l_list, psfp3l_list, psfp4l_list):
    result_dict = {}

    result_dict["avg_psfpl"] = mean(psfpl_list)
    result_dict["avg_psfp2l"] = mean(psfp2l_list)
    result_dict["avg_psfp3l"] = mean(psfp3l_list)
    result_dict["avg_psfp4l"] = mean(psfp4l_list)

    result_dict["std_dev_psfpl"] = stdev(psfpl_list, xbar=result_dict["avg_psfpl"])
    result_dict["std_dev_psfp2l"] = stdev(psfp2l_list, xbar=result_dict["avg_psfp2l"])
    result_dict["std_dev_psfp3l"] = stdev(psfp3l_list, xbar=result_dict["avg_psfp3l"])
    result_dict["std_dev_psfp4l"] = stdev(psfp4l_list, xbar=result_dict["avg_psfp4l"])

    result_dict["variance_psfpl"] = variance(psfpl_list, xbar=result_dict["avg_psfpl"])
    result_dict["variance_psfp2l"] = variance(psfp2l_list, xbar=result_dict["avg_psfp2l"])
    result_dict["variance_psfp3l"] = variance(psfp3l_list, xbar=result_dict["avg_psfp3l"])
    result_dict["variance_psfp4l"] = variance(psfp4l_list, xbar=result_dict["avg_psfp4l"])

    return result_dict

def get_psfpw_stats(psfpw_list, psfp2w_list, psfp3w_list, psfp4w_list):
    result_dict = {}

    result_dict["avg_psfpw"] = mean(psfpw_list)
    result_dict["avg_psfp2w"] = mean(psfp2w_list)
    result_dict["avg_psfp3w"] = mean(psfp3w_list)
    result_dict["avg_psfp4w"] = mean(psfp4w_list)

    result_dict["std_dev_psfpw"] = stdev(psfpw_list, xbar=result_dict["avg_psfpw"])
    result_dict["std_dev_psfp2w"] = stdev(psfp2w_list, xbar=result_dict["avg_psfp2w"])
    result_dict["std_dev_psfp3w"] = stdev(psfp3w_list, xbar=result_dict["avg_psfp3w"])
    result_dict["std_dev_psfp4w"] = stdev(psfp4w_list, xbar=result_dict["avg_psfp4w"])

    result_dict["variance_psfpw"] = variance(psfpw_list, xbar=result_dict["avg_psfpw"])
    result_dict["variance_psfp2w"] = variance(psfp2w_list, xbar=result_dict["avg_psfp2w"])
    result_dict["variance_psfp3w"] = variance(psfp3w_list, xbar=result_dict["avg_psfp3w"])
    result_dict["variance_psfp4w"] = variance(psfp4w_list, xbar=result_dict["avg_psfp4w"])

    return result_dict

def get_remaining_nums_stats(prns_list, psfrn_list, draws_per_round_list):
    result_dict = {}

    result_dict["avg_prns"] = mean(prns_list)
    result_dict["avg_psfrn"] = mean(psfrn_list)
    result_dict["avg_draws_per_round"] = mean(draws_per_round_list)

    result_dict["std_dev_prns"] = stdev(prns_list, xbar=result_dict["avg_prns"])
    result_dict["std_dev_psfrn"] = stdev(psfrn_list, xbar=result_dict["avg_psfrn"])
    result_dict["std_dev_draws_per_round"] = stdev(draws_per_round_list, xbar=result_dict["avg_draws_per_round"])

    result_dict["variance_prns"] = variance(prns_list, xbar=result_dict["avg_prns"])
    result_dict["variance_psfrn"] = variance(psfrn_list, xbar=result_dict["avg_psfrn"])
    result_dict["variance_draws_per_round"] = variance(draws_per_round_list, xbar=result_dict["avg_draws_per_round"])

    return result_dict

def get_plirn_stats(pip2lrns_list, psfip2lrn_list):
    result_dict = {}

    result_dict["avg_pip2lrns"] = mean(pip2lrns_list)
    result_dict["avg_psfip2lrn"] = mean(psfip2lrn_list)

    result_dict["std_dev_pip2lrns"] = stdev(pip2lrns_list, xbar=result_dict["avg_pip2lrns"])
    result_dict["std_dev_psfip2lrn"] = stdev(psfip2lrn_list, xbar=result_dict["avg_psfip2lrn"])

    result_dict["variance_pip2lrns"] = variance(pip2lrns_list, xbar=result_dict["avg_pip2lrns"])
    result_dict["variance_psfip2lrn"] = variance(psfip2lrn_list, xbar=result_dict["avg_psfip2lrn"])

    return result_dict
