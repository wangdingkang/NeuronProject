import os
import numpy as np

input_folder = "Iter_Rets/"
ITERATION = 20
KNN = 5

if __name__ == '__main__':
    files = os.listdir(input_folder)
    for file in files:
        print(file)
        ret = []
        with open(input_folder + file) as temp_file:
            for i in range(ITERATION):
                temp_file.readline()
                temp_ret = []
                for k in range(KNN):
                    temp_line = temp_file.readline()
                    vars = temp_line.split('/')
                    temp_ret.append(float(vars[0]) / float(vars[1]))
                ret.append(temp_ret)
            ret_np = np.array(ret)
            variances = np.var(ret_np, axis=0)
            means = np.mean(ret_np, axis=0)
            maxs = np.max(ret_np, axis=0)
            mins = np.min(ret_np, axis=0)
            # print(variances, means, maxs, mins)
            for mi, ma in zip(mins, maxs):
                print('{0:.4f}'.format(mi), '-', '{0:.4f}'.format(ma))
