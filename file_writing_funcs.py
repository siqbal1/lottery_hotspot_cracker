import json

def write_list_to_file(any_list, f_name):

    fp = open(f_name, "w+")

    for elem in any_list:
        fp.write(str(elem) + "\n")


    fp.close()

def write_mean_list_to_file(mean_list, overall_mean, f_name):
    f = open(f_name, 'w')

    f.write("Overall Mean: " + str(overall_mean) + "\n")

    for sample_mean in mean_list:
        f.write(str(sample_mean) + "\n")

    f.close()

def write_dict_to_file(any_dict, f_name):
    with open(f_name, "w") as json_file:
        json.dump(any_dict, json_file)
