import numpy as np

input_file1 = 'distance_mat/L1/distances_23478_removed.txt'
input_file2 = 'distance_mat/L1/distances_dp.txt'

if __name__ == '__main__':
    data1, data2 = [], []

    with open(input_file1, 'r') as file:
        next(file)
        data1 = [list(map(float, line.split())) for line in file if line.strip() != ""]

    with open(input_file2, 'r') as file:
        next(file)
        data2 = [list(map(float, line.split())) for line in file if line.strip() != ""]


    np_data1 = np.array(data1)
    np_data2 = np.array(data2)
    # print(np_data1.shape)
    # print(np_data2.shape)
    max1 = np_data1.max()
    max2 = np_data2.max()
    np_data1 = np.divide(np_data1, max1)
    np_data2 = np.divide(np_data2, max2)
    np_weight = np.add(np.multiply(np_data1, 0.5), np.multiply(np_data2, 0.5))
