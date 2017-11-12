###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
import numpy as np
from operator import itemgetter 

pos = {}
words = {}
wordPos = {}
transitions = np.zeros((12, 12), dtype=np.int_)
initial = {}
initial = {"adj": 0, "adv": 0, "adp": 0, "conj": 0, "det": 0, "noun": 0, "num": 0, "pron": 0, "prt": 0, "verb": 0, "x": 0, ".": 0}
posIDX = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def posterior(self, sentence, label):
		return 0

	# Do the training!
	#
	def train(self, data):
		posCount = 0
		for i in range(0, len(data), 1):
			for j in range(0, len(data[i][0]), 1):
				# part of speech and its count
				posKey = data[i][1][j]
				pos[posKey] = pos[posKey] + 1 if posKey in pos else 1
				if not posKey in posIDX:
					posIDX.append(posKey)
					posIDX.sort()
					initial[posKey] = 0
				# word and its count
				wordKey = data[i][0][j]
				# word & parts of speech and its count
				if wordKey in wordPos:
					posTag = wordPos[wordKey]
					posTag[posKey] = posTag[posKey] + 1 if posKey in posTag else 1
				else:
					posDict = {posKey: 1}
					wordPos[wordKey] = posDict

				if j > 0:
					prevPOS = data[i][1][j - 1]
					transitions[posIDX.index(prevPOS), posIDX.index(posKey)] += 1
				else:
					initialPOS = data[i][1][j]
					initial[initialPOS] += 1
		for word in wordPos.keys():
			words[word] = sum(wordPos[word].values())


	# Functions for each algorithm.
	#
	def simplified(self, sentence):
		listPOS = []
		for word in sentence:
			maxProb = 0.0
			maxPOS = ''
			for p in pos:
				if p in posIDX:
					a = ((wordPos[word][p] + 1 if p in wordPos[word] else 1) if word in wordPos else 1) * 1.0
					b = (pos[p] + len(words)) * 1.0
					c = (pos[p] + 1) * 1.0
					d = (sum(pos.values()) + 1) * 1.0
					simplifiedProb = ((a / b) * (c / d))
					if simplifiedProb > maxProb:
						maxProb = simplifiedProb
						maxPOS = p
			listPOS.append(maxPOS)
		return listPOS

	def hmm_ve(self, sentence):
		posList = []
		prevState = np.zeros([12], np.float_)
		currentState = np.zeros([12], np.float_)
		for idx, word in enumerate(sentence):
			for currentPOS in posIDX:
				emmission = 1.0 * (wordPos[word][currentPOS] + 1 if word in wordPos and currentPOS in wordPos[word] else 1) / (pos[currentPOS] + len(words))
				prevStateSum = 0
				if idx == 0:
					prevStateSum = 1.0 * initial[currentPOS] / sum(initial.values())
				else:
					for prevPOS in posIDX:
						transition = 1.0 * transitions[posIDX.index(prevPOS), posIDX.index(currentPOS)] / pos[prevPOS]
						prevStateSum += transition * prevState[posIDX.index(prevPOS)]
				currentState[posIDX.index(currentPOS)] = prevStateSum * emmission

			posList.append(posIDX[np.argmax(currentState)])
			prevState = currentState
			currentState = np.zeros([12], np.float_)

		return posList

	def hmm_viterbi(self, sentence):
		viterbi = {}
		for wordCnt,word in enumerate(test_data[rowCnt][0]):
			for pos in posIDX:
				maxViterbi = 0
				maxPos = ''
				emissionProb = math.log(1 if not word in wordPos else 1 if not pos in wordPos[word] else wordPos[word][pos]/pos[pos])
				if wordCnt == 0:
					initialProb = math.log(initial[pos]) - math.log(sum(initial.values()))
					matrixScore = emissionProb + initialProb
					viterbi[(posIDX.index(pos),wordCnt)] = ('None',matrixScore)
				else:
					for prevPos in posIDX:
						transValue = 1 if (transitions[posIDX.index(prevPos),posIDX.index(pos)]) <= 1 else (transitions[posIDX.index(prevPos),posIDX.index(pos)])
						transProb = math.log(transValue) - math.log(pos[prevPos])
						interViterbi = (viterbi[posIDX.index(prevPos),wordCnt-1][1] + transProb)*-1
						if interViterbi > maxViterbi:
							maxPos = prevPos
							maxViterbi = interViterbi
					viterbi[(posIDX.index(pos),wordCnt)] = (maxPos,maxViterbi + emissionProb)
		returnList = [maxPos]
		for wordCnt in range(len(test_data[rowCnt][0])-1,-1,-1):
			posList = []
			for key, value in viterbi.items():   # iter on both keys and values
				if key[1] == wordCnt:
					posList.append(value)
			maxPos = max(posList,key=itemgetter(1))[0]
			returnList.insert(0,maxPos)
	# This solve() method is called by label.py, so you should keep the interface the
	#  same, but you can change the code itself. 
	# It should return a list of part-of-speech labelings of the sentence, one
	#  part of speech per word.
	#
	def solve(self, algo, sentence):
		if algo == "Simplified":
			return self.simplified(sentence)
		elif algo == "HMM VE":
			return self.hmm_ve(sentence)
		elif algo == "HMM MAP":
			return self.hmm_viterbi(sentence)
		else:
			print
			"Unknown algo!"
