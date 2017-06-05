import os
from random import shuffle
from shutil import copyfile

input_folder = 'neurons\\'
output_folder = 'subsampled\\'
subsampled_size = 900

if __name__ == '__main__':

    print('Read in.\n')
    samples = []
    for root, dirs, files in os.walk(input_folder, topdown=False):
        for name in files:
            samples.append(os.path.join(root, name))

    for i in range(20):
        print('Subsampling ' + str(i) + '.\n')
        shuffle(samples)
        sampled = samples[:subsampled_size]

        output_root = output_folder + str(i)
        for file in sampled:
            cor_dir = file[file.find('\\'):file.rfind('\\')]
            # print(cor_dir)
            cor_path = file[file.find('\\'):]
            # print(cor_path)
            if not os.path.exists(output_root + cor_dir):
                os.makedirs(output_root + cor_dir)
            copyfile(file, output_root + cor_path)

        # output_dirs = os.listdir(output_root)
        # for output_dir in output_dirs:
        #     output_files = os.listdir(output_root + '/' + output_dir)
        #     if len(output_files) == 1:
        #         file_remove = output_root + '/' + output_dir + '/' + output_files[0]
        #         dir_remove = output_root + '/' + output_dir
        #         os.remove(file_remove)
        #         os.rmdir(dir_remove)

    print('Refining.\n')
    for root, dirs, samples in os.walk(output_folder, topdown=False):
        for name in dirs:
            path = os.path.join(root, name)
            sub_files = os.listdir(path)
            if len(sub_files) == 0:  # dir has no file
                os.rmdir(path)
            if len(sub_files) == 1 and not os.path.isdir(
                    os.path.join(path, sub_files[0])):  # dir has only one single file
                os.remove(os.path.join(path, sub_files[0]))
                os.rmdir(path)

