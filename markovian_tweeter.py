import tweepy #https://github.com/tweepy/tweepy
import random
import string
import utils

class markovian_tweeter(object):

    def __init__(self):
        self.dict = {}
        self.tweets = self.get_tweets()

    def get_tweets(self):
        #perform OAuth authentication, and initialize tewwpy
        auth = tweepy.OAuthHandler(utils.CONSUMER_KEY, utils.CONSUMER_SECRET)
        api = tweepy.API(auth)

        #create and fill a list of recent tweets
        tweets = []
        recent_tweets = api.user_timeline(id = utils.SCREEN_NAME, count = utils.NUM_TWEETS)
        for tweet in recent_tweets:
            text = tweet.text
            if "RT" not in text:
                tweets.append(filter(lambda x: x in string.printable, text))
        return tweets

    #strip punctuation from words
    def prepare(self, tweet):
        words = tweet.split()
        for i in range(len(words)):
            if "https" in words[i]:
                words[i] = "https://somesite.com"
        return words

    #prepare markov chain from tweets
    def chain_tweets(self):
        for tweet in self.tweets:
            words = self.prepare(tweet)
            start = 0
            while start < len(words) - 2:
                prevWord = (words[start], words[start + 1])
                nextWord = words[start + 2]
                if prevWord not in self.dict:
                    self.dict[prevWord] = [nextWord]
                else:
                    self.dict[prevWord].extend([nextWord])
                start += 1

    #creates tweet using the created markov chain
    def create_tweet(self):
        #grab some words from a pre-existing tweet, just to start the chain
        tweet = self.tweets[random.randint(0, len(self.tweets) - 1)].split()
        seed = []
        chars = 0
        gen_tweet = []
        for index in range(utils.CORPUS):
            word = tweet[index]
            seed.append(word)
        while True:
            words = tuple(seed)
            removedWord = seed.pop(0)
            gen_tweet.append(removedWord)
            if words in self.dict:
                seed.append(random.choice(self.dict[words]))
            else:
                gen_tweet.append(seed.pop(0))
                break
        return ' '.join(gen_tweet)


tweeter = markovian_tweeter()
tweeter.chain_tweets()
for i in range(10):
    print(tweeter.create_tweet())
    print("")
