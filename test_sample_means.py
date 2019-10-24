from statistics import mean

sample_num = input("Enter sample mean list to process:")
file_name = "s" + sample_num + "_stats/sample_means_list_sample_" + sample_num + ".txt"
print(file_name)

with open(file_name, "r") as f:
    #skip first line
    f.readline()
    mean_list = []

    #print mean every 15 draws
    count = 0
    sample_mean = 0
    sample_count = 0

    line = f.readline()
    while line:
        if(count < 15):
            print(count, ":", line)
            float_mean = float(line)
            sample_mean += float_mean
            count += 1
        else:
            #reached 15 means to sample
            #save sample mean
            sample_mean /= count
            mean_list.append(sample_mean)

            print("Sample mean", sample_count, ":", sample_mean)

            count = 0
            sample_mean = 0
            sample_count += 1

        line = f.readline()

    f.close()

    print(mean_list)

    overall_mean = mean(mean_list)

    print("Overall Mean:", overall_mean)
