import os
import re
import pickle
import nltk
import random

def load_tweets():
    # returns a boolean if there was anything loaded
    try:
        tweet_file = open('tweets.pickle', 'r')
        return pickle.load(tweet_file)
    except (EOFError, IOError):
        return None

def load_corpus():
    try:
        with open('markov_model.pickle', 'r') as f:
            return pickle.load(f)
    except (EOFError, IOError):
        return None

def make_model():
    corpus = load_corpus()
    tweets = load_tweets()
    if not tweets:
        return

    if not corpus:
        corpus = []
        for tweet in tweets:
            tweet_tokens = nltk.word_tokenize(tweet.decode('utf-8'))
            tweet_tags = nltk.pos_tag(tweet_tokens)
            corpus += [nltk.pos_tag(tweet_tokens)]

    tag_set = nltk.unique_list(tag for sent in corpus for (word,tag) in sent)
    symbols = nltk.unique_list(word for sent in corpus for (word,tag) in sent)

    trainer = nltk.tag.HiddenMarkovModelTrainer(tag_set, symbols)

    train_corpus = []
    test_corpus = []
    for i in range(len(tweets)):
        if i % 10:
            train_corpus += [tweets[i]]
        else:
            test_corpus += [tweets[i]]

    save_corpus(corpus)
    hmm = train_and_test(trainer, tweets)
    save_model(hmm)
    tweet = ''
    sample = hmm.random_sample(random.Random(), 20)
    for word in sample:
        tweet += word + ' '

def train_and_test(trainer, tweets):
    seq = [map(lambda x:(x,''), nltk.word_tokenize(tweet.decode('utf-8'))) for tweet in tweets]
    hmm = trainer.train_unsupervised(seq, max_iterations=5)
    return hmm

def save_model(model):
    with open('markov_model.pickle', 'w') as f:
        pickle.dump(model, f)
        f.close()

def save_corpus(corpus):
    with open('corpus.pickle', 'w') as f:
        pickle.dump(corpus, f)
        f.close()


if __name__ == '__main__':
    print make_model()
