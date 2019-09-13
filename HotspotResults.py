from statistics import mean
from statistics import stdev
from statistics import variance
from statistics import median
from datetime import date

NUM_SPOTS_PLAYED = 20

class HotspotResults:
    def __init__(self):
        #list of winning nums include bonus
        self.spot_list = []
        #bonus number
        self.bonus = -1

        self.draw_num = 0
        #date object
        self.date = None

        #stats on current draw num
        self.avg = 0
        self.std_dev = 0
        self.variance = 0
        self.median = 0
        self.avg_distance = 0

        #avg distance between spots selected
        self.avg_distance = 0

    # def __init__(self, spots, bonus, draw_num, date):
    #     self.spot_list = spots
    #     self.bonus = bonus
    #     self.draw_num = draw_num
    #     self.date = date
    #
    #     self.avg = set_avg()
    #     self.std_dev = set_std_dev()
    #     self.variance = set_variance()
    #     self.median = set_median()
    #
    #     self.draw_num = draw_num
    #     self.date = date

    def set_avg(self):
        #set avg from spot list elements
        if not self.spot_list:
            print("Error: Spot list not initialized or empty.")
        else:
            self.avg = mean(self.spot_list)

    def set_std_dev(self):
        if not self.spot_list:
            print("Error: Spot list not initialized or empty.")
        else:
            self.std_dev = stdev(self.spot_list, xbar= self.avg)

    def set_variance(self):
        if not self.avg:
            print("Error: Calculate avg before variance")

        else:
            self.variance = variance(self.spot_list, xbar=self.avg)

    def set_median(self):
        if not self.spot_list:
            print("Error: Spot list not initialized or empty.")
        else:
            self.median = median(self.spot_list)

    def set_avg_distance(self):
        if not self.spot_list:
            print("Error: Spot list not initialized or empty.")
        else:
            #n spots in spot list
            #n-1 pairs
            #find avg distance between i-1 & i
            i = 0;
            sum_distance = 0

            #numbers in spots are asscending so no negatives
            while i < (NUM_SPOTS_PLAYED - 1):
                sum_distance += self.spot_list[i + 1] - self.spot_list[i]
                i += 1

            #total distance / (# pairs)
            self.avg_distance = sum_distance / (NUM_SPOTS_PLAYED - 1)


    def set_spot_list(self, s_list):
        if not s_list:
            print("Error: Spot list is empty.")
        else:
            self.spot_list = s_list

            #calculate stats on list
            self.set_avg()
            self.set_std_dev()
            self.set_variance()
            self.set_median()
            self.set_avg_distance()

    def set_bonus(self, bonus_spot):
        self.bonus = bonus_spot

    def set_date(self, date):
        #use date object
        self.date = date

    def set_draw_num(self, draw_num):
        self.draw_num = draw_num

    def __str__(self):
        ret_str = str(self.date) + " "
        ret_str += str(self.draw_num)
        ret_str += "\nSpots:\n"
        ret_str += str(self.spot_list)
        ret_str += "\nBonus: " + str(self.bonus)
        ret_str += "\nMean: " + str(self.avg)
        ret_str += "\nStd_dev: " + str(self.std_dev)
        ret_str += "\nVariance: " + str(self.variance)
        ret_str += "\nMedian: " + str(self.median)
        ret_str += "\nAvg Distance: " + str(self.avg_distance) + "\n"

        return ret_str
