from temp import read_value
import math
def read_do():
    temp = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47
    ]

    d_o = [
    14.6,
    14.22,
    13.8,
    13.44,
    13.08,
    12.76,
    12.44,
    12.11,
    11.83,
    11.56,
    11.29,
    11.04,
    10.76,
    10.54,
    10.31,
    10.06,
    9.86,
    9.64,
    9.47,
    9.27,
    9.09,
    8.91,
    8.74,
    8.57,
    8.41,
    8.25,
    8.11,
    7.96,
    7.83,
    7.68,
    7.56,
    7.43,
    7.3,
    7.17,
    7.06,
    6.94,
    6.84,
    6.72,
    6.6,
    6.52,
    6.4,
    6.33,
    6.23,
    6.13,
    6.06,
    5.97,
    5.88,
    5.79
    ]

    xin = read_value()
    if xin in temp:
        index = temp.index(xin)
        return d_o[index]
    else:
        new = temp
        new.append(xin)
        new = sorted(new)
        print(new)
        new_x = sorted(new)
        max_index = temp.index(math.trunc(xin)) 
        min_index = max_index + 1
        yout = d_o[min_index] + ((xin - temp[min_index]) * (d_o[max_index] - d_o[min_index]) / (temp[max_index] - temp[min_index]))
        return yout 




