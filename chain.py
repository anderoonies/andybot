import random
import os
import pickle

tweet_file_path = os.path.join(os.path.dirname(__file__), 'tweets.pickle')
triple_file_path	 = os.path.join(os.path.dirname(__file__), 'triples.pickle')

class Markov():
	def __init__(self):
		self.dict = {}
		self.words = []

	def store_triples(self):
		with open(triple_file_path, 'wb') as triple_file:
			pickle.dump(self.dict, triple_file)

	def load_tweets(self):
		# returns a boolean if there was anything loaded
		try:
			tweet_file = open(tweet_file_path, 'rb')
			self.tweets = pickle.load(tweet_file)
		except (EOFError, IOError):
			self.tweets = []

	def load_triples(self):
		try:
			triple_file = open(triple_file_path, 'rb')
			self.dict = pickle.load(triple_file)
		except (EOFError, IOError):
			self.dict = {}

	def make_words(self):
		words = []
		for tweet in self.tweets:
			for word in tweet.split():
				words.append(word)
		self.words = words

	def generate_triples(self):
		if len(self.words) < 3:
			return

		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])

	def populate(self):
		# populate the dictionary with keys of two words, values of resulting words
		for word1, word2, word3 in self.generate_triples():
			key = (word1, word2)
			if key in self.dict:
				self.dict[key].append(word3)
			else:
				self.dict[key] = [word3]

	def make_tweet(self, size=140):
		if not self.words:
			self.make_words()

		tweet = ''
		word1_index = random.randint(0, len(self.words) - 3)
		word1 = self.words[word1_index]
		#'|' is the end of tweet character: keep scanning until we don't have one
		while word1.endswith('|'):
			word1_index = random.randint(0, len(self.words) - 3)
			word1 = self.words[word1_index]
		word1, word2 = self.words[word1_index], self.words[word1_index + 1]
		generated_words = ''
		while (len(generated_words) + len(word1) < size):
			generated_words += word1
			if word1.endswith('|'):
				break
			else:
				generated_words += ' '
			print('{}, {} => {}'.format(word1, word2, self.dict[(word1, word2)]))
			word1, word2 = word2, random.choice(self.dict[(word1, word2)])
		if generated_words in self.tweets:
			return self.make_tweet()
		else:
			return generated_words.replace('|', '')
