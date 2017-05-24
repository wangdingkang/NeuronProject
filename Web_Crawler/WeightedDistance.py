import numpy as np

alpha = 0.25

input_file1 = 'distance_mat/L1/distances_dvec.txt'
input_file2 = 'distance_mat/L1/distances_23478_removed.txt'
output_file = 'distance_mat/L1/distances_dvec_L23478_' + str(alpha) + '_' + str(1 - alpha) + '.txt'

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
    np_weight = np.add(np.multiply(np_data1, alpha), np.multiply(np_data2, 1 - alpha))

    with open(output_file, 'w') as file:
        s = len(data1)
        file.write(str(s) + ' ' + str(s) + '\n')
        for row in np_weight.tolist():
            for ele in row:
                file.write('{0:.6f}'.format(ele) + ' ')
            file.write('\n')