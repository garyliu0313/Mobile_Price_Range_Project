
columns = ["battery_power","blue","clock_speed","dual_sim","fc","four_g","int_memory","m_dep","mobile_wt","n_cores","pc","px_height","px_width","ram","sc_h","sc_w","talk_time","three_g","touch_screen","wifi","price_range"]


# Generate dict from columns
columns_dict = {}
for i in range(len(columns)):
    columns_dict[columns[i]] = i

bins = {"battery_power": [500,1000,1500,2000], "clock_speed": [0.5, 1.0, 1.5, 2.0, 2.5,3.0],
        "fc": [0, 5, 10, 15,20], "int_memory": [16,32,48,64],
        "m_dep": [0, 0.25, 0.5, 1.0], "mobile_wt": [70,140,200], "n_cores": [2,4,6,8],
        "pc": [0, 5,10, 15,20], "px_height": [500, 1000, 1500, 2000], "px_width": [500, 1000, 1500, 2000],
        "ram": [500, 1000, 2000, 3000,4000], "sc_h": [5, 10, 15, 20], "sc_w": [5, 10, 15, 20],
        "talk_time": [5, 10, 15, 20]}


# General function for placing a value into an appropriate bin
def place_into_bin(val, breakpoints):
    for index in range(1, len(breakpoints)):
        if val <= breakpoints[index]:
            return breakpoints[index - 1]
    return breakpoints[-1]

def num_to_bool(val):
    if val == 1:
        return "TRUE"
    return "FALSE"


# Attribute names mapped to their changing function
changes = {"blue": num_to_bool, "dual_sim": num_to_bool, "four_g": num_to_bool, "three_g": num_to_bool, "touch_screen": num_to_bool}


def main():
    inputCSV = open("mobile_price_range.csv")
    outputCSV = open("processed.csv", "w")

    for line in inputCSV:
        arr = line.rstrip().split(',')

        for i in range(len(arr)):
            attribute = columns[i]

            trueName = attribute

            # See if the attribute is one of which needs to be made discrete
            if trueName in bins:
                outputCSV.write(str(place_into_bin(float(arr[i]), bins[trueName])))
            # If it needs to undergo a changing function
            elif trueName in changes:
                outputCSV.write(str(changes[trueName](float(arr[i]))))
            # If it remains the same
            else:
                outputCSV.write(arr[i])

            outputCSV.write("\n" if i == len(arr) - 1 else ",")

    inputCSV.close()
    outputCSV.close()


if __name__ == "__main__":
    main()