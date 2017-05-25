import os
from shutil import copyfile

input_neuron = 'old_dataset/'
input_info = 'crawled/'
output = 'crawled_transfer_to_old/'

if __name__ == '__main__':

    dict = {}

    dirs = os.listdir(input_info)
    for dir in dirs:
        files = os.listdir(input_info + dir)
        for file in files:
            dict[file.split('.')[0]] = input_info + dir + '/' + file

    dirs = os.listdir(input_neuron)
    for dir in dirs:
        files = os.listdir(input_neuron + dir)
        for file in files:
            src = dict[file.split('.')[0]]
            dst_dir = output + dir
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            dst = dst_dir + '/' + file.split('.')[0] + '.txt'
            copyfile(src, dst)