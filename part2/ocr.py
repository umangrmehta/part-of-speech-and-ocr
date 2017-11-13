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
import re

letPtnTrn = {}
letPtnTst = {}

train_text = "SAAS PREFACE If a preface is a light which should serve to illumine the contents of a volume, I choose, not words, but human figures to illustrate this little book intended to enter families where children are growing up. I therefore recall here, as an eloquent symbol, Helen Keller and Mrs. Anne Sullivan Macy, who are, by their example, both teachers to myself and, before the world, living documents of the miracle in education. In fact, Helen Keller is a marvelous example of the phenomenon common to all human beings the possibility of the liberation of the imprisoned spirit of man by the education of the senses. Here lies the basis of the method of education of which the book gives a succinct idea. If one only of the senses sufficed to make of Helen Keller a woman of exceptional culture and a writer, who better than she proves the potency of that method of education which builds on the senses? If Helen Keller attained through exquisite natural gifts to an elevated conception of the world, who better than she proves that in the inmost self of man lies the spirit ready to reveal itself? Helen, clasp to your heart these little children, since they, above all others, will understand you. They are your younger brothers when, with bandaged eyes and in silence, they touch with their little hands, profound impressions rise in their consciousness, and they exclaim with a new form of happiness see with my hands. They alone, then, can fully understand the drama of the mysterious privilege your soul has known. When, in darkness and in silence, their spirit left free to expand, their intellectual energy redoubled, they become able to read and write without having learnt, almost as it were by intuition, they, only they, can understand in part the ecstasy which God granted you on the luminous path of learning. Maria Montessori."

train_arr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
transitions = np.zeros((len(train_arr), len(train_arr)), dtype=np.int_)

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25

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
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
#print train_letters['a']
## Below is just some sample code to show you how the functions above work. 
# You can delete them and put your own code here!

str=""
count = 0

for ltIDX in range(len(train_text)):
    if ltIDX > 0:
        transitions[train_arr.index(train_text[ltIDX - 1]), train_arr.index(train_text[ltIDX])] += 1

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
        matchAlpha = 0
        for idx in range(len(letPtnTrn[alphabet])):
            if letPtnTrn[alphabet][idx] == letter[idx]:
                matchAlpha += 1
        tempDict[alphabet] = matchAlpha / (14.0 * 25.0)
    testAplha["".join([ r for r in letter])] = tempDict

for word in test_letters:
    letter = [item for row in word for item in row]
    #print max(testAplha["".join([ r for r in letter])], key=testAplha["".join([ r for r in letter])].get)
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
