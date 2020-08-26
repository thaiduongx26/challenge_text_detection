from process import draw
import cv2
import os
from tqdm import tqdm
if __name__ == "__main__":
    min_w = 1000000000
    min_h = 1000000000
    list_imgs = os.listdir('data/images')
    for img_name in tqdm(list_imgs):
        img = cv2.imread(os.path.join('data/images', img_name))
        if img.shape[0] < min_h:
            min_h = img.shape[0]
        if img.shape[1] < min_w:
            min_w = img.shape[1]

    print('min_h: ', min_h)
    print('min_w: ', min_w)