#!/usr/bin/python
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2017)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np
import string

letPtnTrn = {}
letPtnTst = {}
transitions = np.zeros((12, 12), dtype=np.int_)

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

def read_data(fname):
    exemplars = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w.lower() for w in line.split()])
        exemplars += [ (data[0::2]), ]
    return exemplars

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print (im.size)
    #print (int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '1' if px[x, y] < 1 else '0' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname, train_file) = sys.argv[1:]
train_data = read_data(train_file)
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
#print train_letters['a']
## Below is just some sample code to show you how the functions above work. 
# You can delete them and put your own code here!
train_arr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
str=""
count = 0

for sentence in train_data:
    for words in sentence[0]:
        for ltIDX in len(words):
            if ltIDX > 0:
                transitions[train_arr.index(words[ltIDX - 1]), train_arr.index(words[ltIDX])] += 1
print (transitions)

for i in train_arr:
    letter = train_letters[i]
    letterList = []
    for x in range(len(letter)):
        for y in range(len(letter[0])):
                letterList.append(letter[x][y])
    letPtnTrn[i] = letterList

testAplha = {}
for word in test_letters:
    letter = [item for row in word for item in row]
    tempDict = {}
    for alphabet in letPtnTrn:
        matchAlpha = 1
        for idx in range(len(letPtnTrn[alphabet])):
            if letPtnTrn[alphabet][idx] == letter[idx]:
                matchAlpha *= 0.8
            else:
                matchAlpha *= 0.2
        tempDict[alphabet] = matchAlpha
    testAplha["".join([ r for r in letter])] = tempDict

#print (testAplha)
for letter in testAplha:
    print (max(testAplha[letter], key=testAplha[letter].get))
# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
#print ("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
#for cnt in range(len(test_letters)):
#    print ("\n".join([ r for r in test_letters[cnt] ]))

#print ("\n".join([ r for r in test_letters[19] ]))
#print ("\n".join([ r for r in test_letters[23] ]))
