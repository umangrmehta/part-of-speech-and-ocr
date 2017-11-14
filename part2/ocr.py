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
import math


CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    # print (im.size)
    # print (int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['1' if px[x, y] < 1 else '0' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
# print train_letters['a']
## Below is just some sample code to show you how the functions above work.
# You can delete them and put your own code here!

bitmaps = {}
letPtnTst = {}

characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
transitions = np.zeros((len(characters), len(characters)), dtype=np.int_)
charCount = {}
initial = {}
for c in characters:
    initial[c] = 0
    charCount[c] = 0

file = open(train_txt_fname, 'r');
for line in file:
    for ltIDX in range(len(line)):
        if line[ltIDX] in characters:
            charCount[line[ltIDX]] += 1
        if ltIDX == 0 and (line[ltIDX] in characters):
            initial[line[ltIDX]] += 1
        if ltIDX > 0:
            if line[ltIDX - 1] not in characters or line[ltIDX] not in characters:
                ltIDX += 1
            else:
                transitions[characters.index(line[ltIDX - 1]), characters.index(line[ltIDX])] += 1

totalCharCount = sum(charCount.values())
totalInitials = sum(initial.values())

for i in characters:
    letter = train_letters[i]
    letterList = []
    for x in range(len(letter)):
        for y in range(len(letter[0])):
            letterList.append(letter[x][y])
    bitmaps[i] = letterList

pixelProb = np.zeros((CHARACTER_HEIGHT, CHARACTER_WIDTH), dtype=np.int_)
emissionProb = np.zeros((CHARACTER_HEIGHT, CHARACTER_WIDTH), dtype=np.int_)

for i in range(len(characters)):
    character = characters[i]
    for rowIDX in range(len(train_letters[character])):
        trainRow = list(train_letters[character][rowIDX])
        testRow = list(test_letters[i][rowIDX])
        for colIDX in range(len(trainRow)):
            if trainRow[colIDX] == testRow[colIDX]:
                emissionProb[rowIDX, colIDX] = pixelProb[rowIDX, colIDX] / (float)(CHARACTER_HEIGHT*CHARACTER_WIDTH)

print emissionProb

for bitmap in train_letters:
    for rowIDX, row in enumerate(bitmap):
        for colIDX, pixel in enumerate(row):
            if bitmap:
                pixelProb[rowIDX, colIDX] += 1


def simplified(sentence):
    charList = []
    for charSegment in sentence:
        flatSegment = [item for row in charSegment for item in row]
        maxProb = 0.0
        maxPOS = ''
        for currentChar in bitmaps:
            matchAlpha = 0
            for idx in range(len(bitmaps[currentChar])):
                if bitmaps[currentChar][idx] == flatSegment[idx]:
                    matchAlpha += 1
            simplifiedProb = matchAlpha / (14.0 * 25.0)
            if simplifiedProb > maxProb:
                maxProb = simplifiedProb
                maxPOS = currentChar

        charList.append(maxPOS)
    return charList


def hmm_ve(sentence):
    charList = []
    prevState = np.zeros([len(characters)], np.float_)
    currentState = np.zeros([len(characters)], np.float_)
    for charIDX, charSegment in enumerate(sentence):
        flatSegment = [item for row in charSegment for item in row]
        for currentChar in characters:
            matchAlpha = 1.0
            for idx in range(len(bitmaps[currentChar])):
                if bitmaps[currentChar][idx] == flatSegment[idx]:
                    matchAlpha *= 0.8
                else:
                    matchAlpha *= 0.2
            emission = matchAlpha
            prevStateSum = 0
            if charIDX == 0:
                prevStateSum = 1.0 * initial[currentChar] / totalInitials
            else:
                for prevChar in characters:
                    transition = 1.0 * (transitions[characters.index(prevChar), characters.index(currentChar)] + 1) / (charCount[prevChar] + 1 if charCount[prevChar] > 0 else totalCharCount)
                    prevStateSum += transition * prevState[characters.index(prevChar)]
            currentState[characters.index(currentChar)] = prevStateSum * emission

        charList.append(characters[np.argmax(currentState)])
        prevState = currentState
        currentState = np.zeros([len(characters)], np.float_)

    return charList


def hmm_viterbi(sentence):
    viterbi = np.empty([len(characters), len(sentence)], dtype=np.float_)
    maxPrevChar = np.empty([len(characters), len(sentence)], dtype='S4')
    for charIDX, charSegment in enumerate(sentence):
        for currentChar in characters:
            flatSegment = [item for row in charSegment for item in row]
            maxViterbi = - float('inf')
            maxChar = ''
            matchAlpha = 1.0
            for idx in range(len(bitmaps[currentChar])):
                if bitmaps[currentChar][idx] == flatSegment[idx]:
                    matchAlpha *= 0.8
                else:
                    matchAlpha *= 0.2
            emissionProb = matchAlpha
            if charIDX == 0:
                initialProb = math.log(initial[currentChar] + 1) - math.log(totalInitials + 1)
                matrixScore = emissionProb + initialProb
                viterbi[(characters.index(currentChar), charIDX)] = matrixScore
                maxPrevChar[(characters.index(currentChar), charIDX)] = ''
            else:
                for prevChar in characters:
                    transValue = 1 if (transitions[characters.index(prevChar), characters.index(currentChar)]) <= 1 else (transitions[characters.index(prevChar), characters.index(currentChar)])
                    transProb = math.log(transValue) - math.log(charCount[prevChar] if charCount[prevChar] > 0 else totalCharCount)
                    interViterbi = (viterbi[characters.index(prevChar), charIDX - 1] + transProb)
                    if interViterbi > maxViterbi:
                        maxChar = prevChar
                        maxViterbi = interViterbi
                # print maxPOS
                viterbi[(characters.index(currentChar), charIDX)] = maxViterbi + emissionProb
                maxPrevChar[(characters.index(currentChar), charIDX)] = maxChar

    lastChar = characters[np.argmax(viterbi, axis=0)[-1]]
    returnList = [lastChar]
    for charIDX in range(len(sentence) - 1, 0, -1):
        prevChar = maxPrevChar[characters.index(lastChar), charIDX]
        returnList.insert(0, prevChar)
        lastChar = prevChar
    return returnList


print "Simplified: " + "".join(simplified(test_letters))
print "HMM VE: " + "".join(hmm_ve(test_letters))
print "HMM Viterbi: " + "".join(hmm_viterbi(test_letters))


# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
# print ("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
# for cnt in range(len(test_letters)):
#    print ("\n".join([ r for r in test_letters[cnt] ]))
