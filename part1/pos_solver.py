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

pos = {}
word = {}
wordPos = {}
transitions = np.zeros((12, 12), dtype=np.int_)
posIDX = {"adj" : 0, "adv" : 1, "adp" : 2, "conj" : 3, "det" : 4, "noun" : 5, "num" : 6, "pron" : 7, "prt" : 8, "verb" : 9, "x" : 10, "." : 11}


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
				posKey = key = data[i][1][j]
				pos[key] = pos[key] + 1 if key in pos else 1
				# word and its count
				wordKey = key = data[i][0][j]
				word[key] = word[key] + 1 if key in word else 1
				# word & parts of speech and its count
				if wordKey in wordPos:
					posTag = wordPos[wordKey]
					posTag[posKey] = posTag[posKey] + 1 if posKey in posTag else 1
				else:
					posDict = {posKey: 1}
					wordPos[wordKey] = posDict

				if j > 0:
					prevPOS = data[i][1][j - 1]
					transitions[posIDX[prevPOS], posIDX[posKey]] += 1

	# Functions for each algorithm.
	#
	def simplified(self, sentence):
		for exemp in sentence:
			for word_exemp in exemp[0]:
				listPOS = []
				max_prob = 0
				max_POS = ''
				# print word
				for p in pos:
					print p
					if word_exemp in wordPos.keys():
						if p in wordPos[word_exemp]:
							a = wordPos[word_exemp][p]
							b = pos[p]
							c = sum(pos.values())
							d = word[word_exemp]
							e = sum(word.values())
							simplifiedProb = ((a / b) * (b / c)) / (d / e)

		return [ "noun" ] * len(sentence)

	def hmm_ve(self, sentence):
		return ["noun"] * len(sentence)

	def hmm_viterbi(self, sentence):
		return ["noun"] * len(sentence)

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
