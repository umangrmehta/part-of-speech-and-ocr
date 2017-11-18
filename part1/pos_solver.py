###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids: aybhimdi-mehtau-vsriniv-a3
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
# W: word; POS: part of speech
##
## Simplified:
##-------------
## It is calculated using the formula: P(POS|W) = P(W|POS)P(POS)/P(W)
## Probability of word is constant and it is ingored for calculating the simplified probability
## => P(POS|W) is directly proportional to P(W|POS)P(POS)
## The maximum of the posterior probability for each word is used to derive its part of speech.
##
## Variable Elimination:
##-----------------------
## References: https://www.cs.cmu.edu/~epxing/Class/10708-14/scribe_notes/scribe_note_lecture4.pdf
## 			   https://www.youtube.com/watch?v=7zDARfKVm7s
## We have used forward-backward algorith for implementing variable elimination using HMM.
## Forward Matrix: stores the initial to final probability (P(POS|W)) score
## Backwar Matrix: stores the final to initial probability (P(POS|W)) score
## For calculating the P(POS|W), each element in the forward matrix is multiplied with the corresponding element in the same cell of the backward matrix
## For each word the maximum probability is calculated, and its respective part of speech is assigned to that word.
## 
## Viterbi:
##----------
## Calculated using the formula : v[t+1] = e(w[t+1]) {for i=1 to N max( v[t]*P(ij)}
## where t+1 is the current word; t is the previous word and e() is the emission probability; v is viterbi value; N is total number of part of speech
## This is Bellman's equation
## We have taken tranformation of this equation: v[t+1] = log(e(w[t+1])) {for i=1 to N argmax( log(v[t])+log(P(ij))}
## We have used two matrices
##	- store the value for posterior
##	- store the part of speech max value for that character
## 
## Posterior:
##------------ 
## Followed the simplified probability calculation technique to display the sentence accuracy.
## 
#

####

import math
import numpy as np

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling
	def __init__(self):
		self.pos = {}
		self.words = {}
		self.totalWords = 0
		self.wordPos = {}
		self.transitions = np.zeros((12, 12), dtype=np.int_)
		self.initial = {"adj": 0, "adv": 0, "adp": 0, "conj": 0, "det": 0, "noun": 0, "num": 0, "pron": 0, "prt": 0, "verb": 0, "x": 0, ".": 0}
		self.posIDX = ["adj", "adv", "adp", "conj", "det", "noun", "num", "pron", "prt", "verb", "x", "."]

	def posterior(self, sentence, label):
		sumOfpostProb = 0
		for i in range(0,len(sentence)):
			postProb = 0
			word = sentence[i]
			p = label[i]
			a = math.log(1.0 * self.wordPos[word][p] / self.pos[p] if word in self.wordPos and p in self.wordPos[word] else 1.0 / (2.0 * self.totalWords))
			b = math.log(self.pos[p] + 1)
			c = math.log((sum(self.pos.values()) + 1) * 1.0)
			postProb = (a + (b - c))
			sumOfpostProb += postProb
		return sumOfpostProb

	# Do the training!
	#
	def train(self, data):
		posCount = 0
		for i in range(0, len(data), 1):
			for j in range(0, len(data[i][0]), 1):
				# part of speech and its count
				posKey = data[i][1][j]
				self.pos[posKey] = self.pos[posKey] + 1 if posKey in self.pos else 1
				if not posKey in self.posIDX:
					self.posIDX.append(posKey)
					self.posIDX.sort()
					self.initial[posKey] = 0
				# word and its count
				wordKey = data[i][0][j]
				# word & parts of speech and its count
				if wordKey in self.wordPos:
					posTag = self.wordPos[wordKey]
					posTag[posKey] = posTag[posKey] + 1 if posKey in posTag else 1
				else:
					posDict = {posKey: 1}
					self.wordPos[wordKey] = posDict

				if j > 0:
					prevPOS = data[i][1][j - 1]
					self.transitions[self.posIDX.index(prevPOS), self.posIDX.index(posKey)] += 1
				else:
					initialPOS = data[i][1][j]
					self.initial[initialPOS] += 1
		for word in self.wordPos.keys():
			self.words[word] = sum(self.wordPos[word].values())

		self.totalWords = sum(self.words.values())


	# Functions for each algorithm.
	#
	def simplified(self, sentence):
		listPOS = []
		for word in sentence:
			maxProb = 0.0
			maxPOS = ''
			for p in self.pos:
				if p in self.posIDX:
					a = 1.0 * self.wordPos[word][p] / self.pos[p] if word in self.wordPos and p in self.wordPos[word] else 1.0 / (2.0 * self.totalWords)
					c = (self.pos[p]) * 1.0
					d = (sum(self.pos.values())) * 1.0
					simplifiedProb = a * (c / d)
					if simplifiedProb > maxProb:
						maxProb = simplifiedProb
						maxPOS = p
			listPOS.append(maxPOS)
		return listPOS

	def hmm_ve(self, sentence):
		forward = np.zeros((12, len(sentence)), dtype=np.float)
		for idx, word in enumerate(sentence):
			for currentPOS in self.posIDX:
				emission = 1.0 * self.wordPos[word][currentPOS] / self.pos[currentPOS] if word in self.wordPos and currentPOS in self.wordPos[word] else 1.0 / (2.0 * self.totalWords)
				prevStateSum = 0
				if idx == 0:
					prevStateSum = 1.0 * self.initial[currentPOS] / sum(self.initial.values())
				else:
					for prevPOS in self.posIDX:
						transition = 1.0 * self.transitions[self.posIDX.index(prevPOS), self.posIDX.index(currentPOS)] / self.pos[prevPOS]
						prevStateSum += transition * forward[self.posIDX.index(prevPOS), idx - 1]
				forward[self.posIDX.index(currentPOS), idx] = prevStateSum * emission

		backward = np.zeros((12, len(sentence)), dtype=np.float)
		for idx in range(len(sentence) - 1, -1, -1):
			word = sentence[idx]
			for currentPOS in self.posIDX:
				emission = 1.0 * self.wordPos[word][currentPOS] / self.pos[currentPOS] if word in self.wordPos and currentPOS in self.wordPos[word] else 1.0 / (2.0 * self.totalWords)
				prevStateSum = 0
				if idx == len(sentence) - 1:
					prevStateSum = 1.0 * self.pos[currentPOS] / self.totalWords
				else:
					for prevPOS in self.posIDX:
						transition = 1.0 * self.transitions[self.posIDX.index(currentPOS), self.posIDX.index(prevPOS)] / self.pos[prevPOS]
						prevStateSum += transition * backward[self.posIDX.index(prevPOS), idx + 1]
				backward[self.posIDX.index(currentPOS), idx] = prevStateSum * emission

		convolution = np.multiply(forward, backward)

		return [self.posIDX[idx] for idx in np.argmax(convolution, axis=0)]

	def hmm_viterbi(self, sentence):
		viterbi = np.empty([12, len(sentence)], dtype=np.float_)
		maxPrevPOS = np.empty([12, len(sentence)], dtype='S4')
		for wordIDX, word in enumerate(sentence):
			for currentPOS in self.posIDX:
				maxViterbi = - float('inf')
				maxPOS = ''
				emissionProb = math.log(1.0 * self.wordPos[word][currentPOS] / self.pos[currentPOS] if word in self.wordPos and currentPOS in self.wordPos[word] else 1.0 / (2.0 * self.totalWords))
				if wordIDX == 0:
					initialProb = math.log(self.initial[currentPOS]) - math.log(sum(self.initial.values()))
					matrixScore = emissionProb + initialProb
					viterbi[(self.posIDX.index(currentPOS), wordIDX)] = matrixScore
					maxPrevPOS[(self.posIDX.index(currentPOS), wordIDX)] = ''
				else:
					for prevPOS in self.posIDX:
						transValue = 1 if (self.transitions[self.posIDX.index(prevPOS), self.posIDX.index(currentPOS)]) <= 1 else (self.transitions[self.posIDX.index(prevPOS), self.posIDX.index(currentPOS)])
						transProb = math.log(transValue) - math.log(self.pos[prevPOS])
						interViterbi = (viterbi[self.posIDX.index(prevPOS), wordIDX - 1] + transProb)
						if interViterbi > maxViterbi:
							maxPOS = prevPOS
							maxViterbi = interViterbi
					# print maxPOS
					viterbi[(self.posIDX.index(currentPOS), wordIDX)] = maxViterbi + emissionProb
					maxPrevPOS[(self.posIDX.index(currentPOS), wordIDX)] = maxPOS

		lastPOS = self.posIDX[np.argmax(viterbi, axis=0)[-1]]
		returnList = [lastPOS]
		for wordIDX in range(len(sentence) - 1, 0, -1):
			prevPOS = maxPrevPOS[self.posIDX.index(lastPOS), wordIDX]
			returnList.insert(0, prevPOS)
			lastPOS = prevPOS
		return returnList

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
