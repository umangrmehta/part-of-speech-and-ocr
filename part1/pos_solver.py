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

pos={}
word={}
wordPos={}

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
		for i in range (0, len(data), 1):
			for j in range (0, len(data[i][0]), 1):
				# part of speech and its count
				posKey = key = data[i][1][j]
				pos[key] = pos[key] + 1 if key in pos else 1
				# word and its count
				wordKey=key = data[i][0][j]
				word[key] = word[key] + 1 if key in word else 1
				# word & parts of speech and its count
				if wordKey in wordPos:
					posTag = wordPos[wordKey]
					posTag[posKey] = posTag[posKey] + 1 if posKey in posTag else 1
				else:
					posDict = {posKey: 1}
					wordPos[wordKey] = posDict


	# Functions for each algorithm.
	#
	def simplified(self, sentence):
		return [ "noun" ] * len(sentence)

	def hmm_ve(self, sentence):
		return [ "noun" ] * len(sentence)

	def hmm_viterbi(self, sentence):
		return [ "noun" ] * len(sentence)


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
			print "Unknown algo!"

