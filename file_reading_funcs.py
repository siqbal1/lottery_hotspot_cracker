import json

def read_list_from_file(f_name):
    """
    open file and read line by line
    return list of line values
    """
    ret_list = list()

    try:
        with open(f_name) as list_file:
            for line in list_file:
                line = line.strip()
                ret_list.append(line)

        return ret_list

    except FileNotFoundError:
        print("Unable to find file", f_name)
        return None

def read_mean_list(f_name):
    """
    open file and read line by line
    return list of line values
    """
    ret_list = list()

    try:
        with open(f_name) as list_file:
            for index, line in enumerate(list_file):
                print(index, line)
                if(index != 0):
                    line = line.strip()
                    line = float(line)
                    ret_list.append(line)

        print(ret_list)

        return ret_list

    except FileNotFoundError:
        print("Unable to find file", f_name)
        return None


def read_dict_from_file(json_file_name):
    """
    read json_file
    return json_dict
    """

    try:
        with open(json_file_name) as json_file:
            ret_dict = json.load(json_file)

            return ret_dict

    except FileNotFoundError:
        print("Unable to find file", json_file_name)
        return None
