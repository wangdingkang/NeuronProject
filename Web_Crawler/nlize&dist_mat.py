import os
import numpy as np
import scipy.spatial.distance as spd

input_folder = 'crawled/'
dist_mat_folder = 'distance_mat/'
normalize_folder = 'normalized_info/'


class NeuronFeature:

    def __init__(self, fp, data):
        self.input_file = fp
        self.data = data
        self.output_file = normalize_folder + fp[fp.find('/'):]

    def z_score(self, means, stds):
        self.data = [(datum - mean) / std for datum, mean, std in zip(self.data, means, stds)]

    def max_min(self, maxs, mins):
        self.data = [(datum - min) / (max - min) for datum, max, min in zip(self.data, maxs, mins)]

    def output(self):
        dir_path = self.output_file[:self.output_file.rfind('/')]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        with open(self.output_file, 'w') as file:
            for datum in self.data:
                file.write(str(datum) + '\n')

def all_input_files():
    ret = []
    dirs = os.listdir(input_folder)
    for dir in dirs:
        files = os.listdir(input_folder + dir)
        for file in files:
            ret.append(input_folder + dir + '/' + file)
    return ret

def read_file(filename):
    ret = []
    with open(filename, 'r') as file:
        for line in file:
            ret.append(float(line.split()[1]))
    return ret

if __name__ == '__main__':
    input_files = all_input_files()
    neurons = []
    # cnt_file = len(input_files)
    data = []
    for input_file in input_files:
        features = read_file(input_file)
        data.append(features)
        neurons.append(NeuronFeature(input_file, features))

    # print(data)
    means = np.mean(np.array(data), axis=0).tolist()
    stds = np.std(np.array(data), axis=0, ddof=1).tolist()

    data = []
    for neuron in neurons:
        neuron.z_score(means, stds)
        data.append(neuron.data)
       # neuron.output()

    np_data = np.array(data)
    pdists = spd.squareform(spd.pdist(np_data, 'euclidean')).tolist()
    with open(dist_mat_folder + 'distances.txt', 'w') as file:
        for row in pdists:
            for ele in row:
                file.write('{0:.6f}'.format(ele) + ' ')
            file.write('\n')