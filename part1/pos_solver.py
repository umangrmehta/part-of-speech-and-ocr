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
				#words[wordKey] = words[wordKey] + 1 if wordKey in word else 1
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
			maxProb = 0
			maxPOS = ''
			# print word
			for p in pos:
				print p
				if word in wordPos:
					if p in wordPos[word]:
						a = wordPos[word][p]
						b = pos[p]
						c = sum(pos.values())
						d = word[word]
						e = sum(word.values())
						simplifiedProb = ((a / b) * (b / c)) / (d / e)
						a = math.log(wordPos[word][p])
						b = math.log(pos[p])
						c = math.log(sum(pos.values()))
						d = math.log(words[word])
						e = math.log(sum(words.values()))
						simplifiedProb = (((1 + a - b) + (b - c)) - (d - e))
						#print "all probabilities:", simplifiedProb
						if simplifiedProb > max_prob:
							max_prob = simplifiedProb
							max_POS = p
						max_prob_final = max_prob
						listPOS.append(max_POS)
					#print "For '", word, "'the POS is ", max_POS_final, " with probability of", max_prob

		return listPOS

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
