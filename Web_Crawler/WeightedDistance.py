import numpy as np
import os

alpha = 0.75

input_folder1 = 'distance_mat/subsample_dvec/'
input_folder2 = 'distance_mat/subsample_dlm/'
file1s = os.listdir(input_folder1)
file2s = os.listdir(input_folder2)

for input_file1, input_file2 in zip(file1s, file2s):
    # input_file1 = 'distance_mat/old_dataset/distances_dvec.txt'
    # input_file2 = 'distance_mat/old_dataset/distances_dvec_23478_L1.txt'
    output_file = 'distance_mat/distances_dvec_dlm_' + str(alpha) + '_' + str(1 - alpha) + '.txt'
    input_file1 = input_folder1 + input_file1
    input_file2 = input_folder2 + input_file2
    print(input_file1, input_file2, output_file)

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
    np_weight = np.add(np.multiply(np_data1, alpha), np.multiply(np_data2, 1 - alpha))

    with open(output_file, 'w') as file:
        s = len(data1)
        file.write(str(s) + ' ' + str(s) + '\n')
        for row in np_weight.tolist():
            for ele in row:
                file.write('{0:.6f}'.format(ele) + ' ')
            file.write('\n')