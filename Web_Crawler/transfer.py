import os
from shutil import copyfile

input_neuron = 'subsampled\\'
input_info = 'crawled\\'
output = 'subsampled_data\\'

if __name__ == '__main__':

    dict = {}

    for root, dirs, files in os.walk(input_info, topdown=False):
        for name in files:
            dict[name.split('.')[0]] = os.path.join(root, name)

    for root, dirs, files in os.walk(input_neuron):
       for name in files:
            src = dict[name.split('.')[0]]
            dst_dir = os.path.join(output, root[root.find('\\') + 1:])
            # print(dst_dir)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            dst = os.path.join(dst_dir, src[src.rfind('\\') + 1:])
            copyfile(src, dst)