import os
import glob
import cv2
import numpy as np
import tqdm


def calc_stats(images_dir, bits):
    mean = np.zeros(3)
    std = np.zeros(3)
    with open('/home/carson/data/m3fd/meta/all.txt', 'r') as f:
        i = 0
        for line in tqdm.tqdm(list(f.readlines())):
            filename = str(line[0:-1]) + '.png'
            fp = os.path.join(images_dir, filename)

            img = cv2.imread(fp, -1) / (2**bits - 1)
            mean += img.mean(axis=(0, 1)).squeeze()
            std += img.std(axis=(0, 1)).squeeze()
            i += 1
        
    print(mean / i, std / i)

images_dir ='/home/carson/data/m3fd/Vis/'
bits = 8

calc_stats(images_dir, bits)
