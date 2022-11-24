from tensorflow.keras.models import Model, load_model
import numpy as np
from PIL import Image
from itertools import chain
from skimage.io import imread, imshow, imread_collection, concatenate_images
from skimage.transform import resize
from itertools import product
from tqdm import tqdm
import math
import sys
import re
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
import os
import glob
import matplotlib.pyplot as plt
import cv2
#from google.colab.patches import cv2_imshow
dir_path = ''

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
model = load_model(resource_path('./my_model_grey_noise_text.h5'))
def resizeAndPad(img, size, padColor):
    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA

    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = float(w)/h
    saspect = float(sw)/sh

    if (saspect > aspect) or ((saspect == 1) and (aspect <= 1)):  # new horizontal image
        new_h = sh
        new_w = np.round(new_h * aspect).astype(int)
        pad_horz = float(sw - new_w) / 2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0

    elif (saspect < aspect) or ((saspect == 1) and (aspect >= 1)):  # new vertical image
        new_w = sw
        new_h = np.round(float(new_w) / aspect).astype(int)
        pad_vert = float(sh - new_h) / 2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0

    # set pad color
    if len(img.shape) is 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img
def tile(filename, dir_in, dir_out):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    print("Input shape of the image is",img.size)
    d = h
    nw = int(w/(int(w / (h +1))))
    nh = h
    grid = product(range(0, h-h%d, d), range(0, w-w%nw, nw))
    n = 0
    diff = d - nw
    for i, j in grid:
        n = n+1
        box = (j, i, j+nw, i+d)
        out = os.path.join(dir_out,str(n)+".png")
        img.crop(box).save(out)
        
    return diff
def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s

def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]
#######################################
#######################################
def UDM(IMAGE,usethreshold,remove_noise):
    if(usethreshold == 1):
      threshold = input("choose the value of the threshold from  1 to 254 >>>>>")
    file_path = r'./validd/'
    if os.path.exists(file_path):
        print('file already exists')
    else:
        os.mkdir(file_path)
    for f in os.listdir('./validd/'):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join('./validd/', f))
    diff = tile (IMAGE,".","./validd")
    #print (diff)
    #######################################
    VALID_PATH = "./validd/"
    valid_ids = sorted(os.listdir(VALID_PATH), key=alphanum_key)
    print(valid_ids)
    X_valid = np.zeros((len(valid_ids), 128, 128), dtype=np.uint8)
    ####################################
    sys.stdout.flush()
    sizes_valid = []
    for n, id_ in tqdm(enumerate(valid_ids), total=len(valid_ids)):
        path = VALID_PATH + id_
        img = cv2.imread(dir_path + path, cv2.IMREAD_GRAYSCALE)[:,:]
        img = resizeAndPad(img, (540, 540), 255)
   
        if(usethreshold == 1):
          (thresh, img) = cv2.threshold(img, int(threshold), 255, cv2.THRESH_BINARY)   
          print("thresholding may have weird effects on the output, it is advised to try the the image as grayscale before")
        sizes_valid.append([img.shape[0], img.shape[1]])
        img = resize(img, (128, 128), mode='constant', preserve_range=True)
        X_valid[n] = img
    print('Done!')
    #####################################
    preds_valid = model.predict(X_valid, verbose=1)
    preds_valid_t = (preds_valid > 0.5).astype(np.uint8)
    preds_valid_upsampled = []
    for i in range(len(preds_valid_t)):
        preds_valid_upsampled.append(resize(np.squeeze(preds_valid_t[i]), 
                                          (sizes_valid[i][0], sizes_valid[i][1]), 
                                          mode='constant', preserve_range=True))
    #######################################

    file_pathh = r'./final_order/'
    if os.path.exists(file_pathh):
        print('file already exists')
    else:
        os.mkdir(file_pathh)
    for f in os.listdir('./final_order/'):
        if not f.endswith(".png"):
            continue
        os.remove(os.path.join('./final_order/', f))
    file_path = r'./final_order/'
    if os.path.exists(file_path):
        print('file already exists')
    else:
        os.mkdir(file_path)
    for x in range(len(preds_valid_t)):
       
        img = np.squeeze(preds_valid_t[x])
        img = img*255   
        opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_GRAY2BGR)
        cv2.imwrite("./final_order/"+str(x)+".png",opencvImage)
       
    #################################
    images = [cv2.imread(file) for file in sorted(glob.glob("./final_order/*.png"), key=alphanum_key)]
    im_h = cv2.hconcat(images)
    if (remove_noise == 1):
      input("removing noise may have weird effects on the output, it is advised to try without denoising before")
      im_h = cv2.fastNlMeansDenoising(im_h)
    cv2.imwrite("./out.png", im_h)
    print('Printing image')
    return cv2.imshow("img",im_h)

while True:
    inpuut = input("please enter path and name of the input image >>>>>")
    UDM(inpuut,0,0)
    print('Image saved in relative path, close image window to proceed...')
    cv2.waitKey(0)
