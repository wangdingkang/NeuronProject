import os
from random import shuffle
from shutil import copyfile

input_folder = 'old_dataset/'
output_folder = 'subsampled/'
subsampled_size = 250

if __name__ == '__main__':

    files = []
    dirs = os.listdir(input_folder)
    for dir in dirs:
        for file in os.listdir(input_folder + dir):
            files.append(input_folder + dir + '/' + file)


    for i in range(20):
        shuffle(files)
        sampled = files[:subsampled_size]

        output_root = output_folder + str(i)
        if not os.path.exists(output_root):
            os.mkdir(output_root)
            for file in sampled:
                cor_dir = file[file.find('/'):file.rfind('/')]
                # print(cor_dir)
                cor_path = file[file.find('/'):]
                # print(cor_path)
                if not os.path.exists(output_root + cor_dir):
                    os.mkdir(output_root + cor_dir)
                copyfile(file, output_root + cor_path)

        output_dirs = os.listdir(output_root)
        for output_dir in output_dirs:
            output_files = os.listdir(output_root + '/' + output_dir)
            if len(output_files) == 1:
                file_remove = output_root + '/' + output_dir + '/' + output_files[0]
                dir_remove = output_root + '/' + output_dir
                os.remove(file_remove)
                os.rmdir(dir_remove)

