import random
import os
import pickle

class Markov():
	def __init__(self):

		with open('/users/andybayer/code/ANDY_3000/tweets.txt', 'r') as tweet_file:
			self.tweets = pickle.load(tweet_file)
		self.dict = {}
		self.words = self.make_words()
		self.populate()
		self.triples()

	def make_words(self):
		words = []
		for tweet in self.tweets:
			for word in tweet.split():
				words.append(word)
		print words
		return words

	def triples(self):
		#generate triples from the words
		if len(self.words) < 3:
			return

		for i in range(len(self.words) -2):
			yield (self.words[i], self.words[i+1], self.words[i+2])

	def populate(self):
		#populate the dictionary with keys of two words, values of resulting words
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.dict:
				self.dict[key].append(w3)
			else:
				self.dict[key] = [w3]

	def make_tweet(self, size=140, topic=""):
		tweet=''
		w1_index = random.randint(0, len(self.words) - 3)
		word1 = self.words[w1_index]
		print word1
		#| is the end of tweet character: keep scanning until we don't have one
		while word1.endswith('|'):
			w1_index = random.randint(0, len(self.words)-3)
			word1 = self.words[w1_index]
		word1, word2 = self.words[w1_index], self.words[w1_index+1]
		generated_words = ''
		while (len(generated_words) + len(word1) < size):
			generated_words += word1
			if word1.endswith('|'):
				break
			else:
				generated_words += ' '
			word1, word2 = word2, random.choice(self.dict[(word1, word2)])
		if generated_words in self.tweets:
			return self.make_tweet()
		else:
			return generated_words.replace('|', '')

# for debugging
# m=Markov(tweets)
# a = m.make_tweet()
# print a
