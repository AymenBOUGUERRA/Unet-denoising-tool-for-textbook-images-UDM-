import random
import cv2
import os
import numpy as np


# assign input directory
directory = 'C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/input'
'''
this function will not only resize the image to the desired x and y but will also pad the missing pixels 
in a way that the initial x/y ratio is respected
pad color is for 0 to 255 in grayscale
'''


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


"""
This function will allow us to add noise in the image
its modified version of the "sald and peper" noise

"""


def add_noise(img):
    # Getting the dimensions of the image
    row, col = img.shape

    # Randomly pick some pixels in the
    # image for coloring them white
    # Pick a random number between 300 and 10000

    # Randomly pick some pixels in
    # the image for coloring them black
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(3000, 7000)
    for i in range(number_of_pixels):
        # Pick a random y coordinate
        y_coord = random.randint(0, row - 2)

        # Pick a random x coordinate
        x_coord = random.randint(0, col - 2)
        colorrr = random.randint(0,127)
        # Color that pixel to black
        img[y_coord][x_coord] = colorrr
        img[y_coord+1][x_coord+1] = colorrr
        img[y_coord+1][x_coord] = colorrr
        img[y_coord][x_coord+1] = colorrr
    return img






"""
This is the main function of our tool:
this function will take a random area of the mask and apply it to the image

with this current application 
it takes a random mask out of 4 possible grids,
apply a grey background with values randomly ranging from 120 to 255
and then add noise with 2 per 2 pixels to the image 
name the files following an index
this too will save combinations of two files, the noisy image and the clean one
"""


def maino(img, grid, filename, i):
    grid_shape = grid.shape
    img_shape = img.shape
    print(filename)
    print(img_shape)
    print(grid_shape)
    if img_shape[0] >= grid_shape[0]*2 or img_shape[1] >= grid_shape[1]*2:
        img = cv2.resize(img, (int(img_shape[1]*0.3), int(img_shape[0]*0.3)))
    if img_shape[0] >= grid_shape[0] or img_shape[1] >= grid_shape[1]:
        img = cv2.resize(img, (int(img_shape[1]*0.5), int(img_shape[0]*0.5)))
    img_shape = img.shape
    print("reshaped", img_shape)
    # inverted_image = cv2.bitwise_not(img)
    x1 = random.randint(0, grid_shape[0]-img_shape[0]-1)
    y1 = random.randint(0, grid_shape[1]-img_shape[1]-1)
    x2, y2 = x1+img_shape[0], y1+img_shape[1]
    crop_rectangle = grid[x1:x2, y1:y2]
    img = resizeAndPad(img, (540, 540), 255)
    crop_rectangle = resizeAndPad(crop_rectangle, (540, 540), 255)
    blend = cv2.addWeighted(img, 0.5, crop_rectangle, 0.5, 0.0)
    # blend = cv2.add(img, crop_rectangle)
    shadow = random.randint(120, 255)
    (thresh, blackAndWhiteImage) = cv2.threshold(blend, 240, 255, cv2.THRESH_BINARY)
    blackAndWhiteImage[blackAndWhiteImage == 255] = shadow
    blackAndWhiteImage = add_noise(blackAndWhiteImage)
    # (thresh, blackAndWhiteImagegrid) = cv2.threshold(crop_rectangle, 240, 255, cv2.THRESH_BINARY)
    (thresh, blackAndWhiteImage_original) = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    cv2.imwrite('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/images_test/' + str(i) + ".png", blackAndWhiteImage)
    cv2.imwrite('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/masks_test/' + str(i) + ".png", blackAndWhiteImage_original)
    return print("Done")
    
# iterate over files in that directory


i = 0


for filename in os.listdir(directory):
    rand = random.randint(2, 5)
    f = os.path.join(directory, filename)
    if rand == 2:
        grid = cv2.imread('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/french_grid.png',
                          cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        maino(img, grid, filename, i)
    if rand == 3:
        grid = cv2.imread('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/lines_grid.png',
                          cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        maino(img, grid, filename, i)
    if rand == 4:
        grid = cv2.imread('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/standard_grid.png',
                          cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        maino(img, grid, filename, i)
    if rand == 5:
        grid = cv2.imread('C:/Users/aymen/PycharmProjects/pythonProject/types_of_interline/no_grid.png',
                          cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
        maino(img, grid, filename, i)
    i = i + 1






