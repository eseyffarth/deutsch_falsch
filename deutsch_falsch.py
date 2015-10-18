__author__ = 'Esther'
import random
import re
import tweepy
from wordnik import *
import deutsch_config
import traceback
import time


dict_path = "D:/Korpora/WordNet/2.1/dict/index.noun"
# This is a workaround for the random dictionary definitions. I use a noun list
# from WordNet (available here: http://wordnet.princeton.edu/wordnet/download/current-version/ )
# from which I can choose a random word whose definition I can then look up at Wordnik.
# I bet someone knows an easier way to look up nouns only on Wordnik. If you do, let me know!

owner = "ojahnn"    # Twitter handle to send error messages to

def login():
    # for info on the tweepy module, see http://tweepy.readthedocs.org/en/
    # Authentication is taken from deutsch_config.py
    consumer_key = deutsch_config.consumer_key
    consumer_secret = deutsch_config.consumer_secret
    access_token = deutsch_config.access_token
    access_token_secret = deutsch_config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


def make_german_word_from_data(uni_file, bi_file, tri_file):
    """
    Generate a German-looking word from unigram, bigram and trigram counts that
    were extracted from a list of actual German words. Return a single word that
    orthographically resembles German.
    """
    unigrams = {}
    uni = open(uni_file, "r", encoding="utf8")
    for line in uni.readlines():
        if len(line) > 0:
            line = line.split("\t", 1)
            unigrams[line[0].strip()] = int(line[1].strip())

    bigrams = {}
    bi = open(bi_file, "r", encoding="utf8")
    for line in bi.readlines():
        if len(line) > 0:
            line = line.split("\t", 1)
            bigrams[line[0].strip()] = int(line[1].strip())

    trigrams = {}
    tri = open(tri_file, "r", encoding="utf8")
    for line in tri.readlines():
        if len(line) > 0:
            line = line.split("\t", 1)
            trigrams[line[0].strip()] = int(line[1].strip())

    starters = ""
    for key in unigrams:
        starters += key * unigrams[key]

    # First character of the word will be chosen from the collection of possible
    # first characters. The collection of starter chars is weighted so that more
    # common first characters are also more likely to be chosen.
    output = random.choice(starters)
    seconds = ""
    for key in bigrams:
        if key.startswith(output):
            seconds += key[-1] * bigrams[key]

    # Same thing happens with the second character of our new word
    output += random.choice(seconds)

    # Now that we have two characters, we can use the trigram data to collect the
    # next characters. Repeat until we hit a word boundary char (#).
    while not output.endswith("#"):
        continuers = ""
        for key in trigrams:
            if key.startswith(output[-2:]):
                continuers += key[-1] * trigrams[key]
        output += random.choice(continuers)
    output = output[:-1]    # remove word boundary marker
    return output

def fetch_rando_definition():
    """
    Connect to the Wordnik API to retrieve a random word definition. Return the definition.
    """

    # You can find out more about the Wordnik API at http://developer.wordnik.com/
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = deutsch_config.wordnik_key
    client = swagger.ApiClient(apiKey, apiUrl)

    wordApi = WordApi.WordApi(client)

    # Open the noun list from WordNet
    nouns = open(dict_path, "r")
    nouns = [line.strip() for line in nouns.readlines() if line[0].isalpha()]
    nouns = [noun.split(" ", 1)[0] for noun in nouns if "_" not in noun.split(" ", 1)[0]]

    while True:
        rando_word = random.choice(nouns)
        try:
            # fetch word definition from wordnik API
            rando_def = wordApi.getDefinitions(rando_word,
                                 partOfSpeech='noun',
                                 sourceDictionaries='wiktionary',
                                 limit=1)[0].text
            # definition may not contain ()[]
            # definition cannot contain a "," in the first 30 chars (in order to
            # avoid relative clauses, enumerations etc)
            if "(" not in rando_def and "[" not in rando_def and "," not in rando_def[:30]:
                rando_def = re.split("[\_\,\.\;\:]", rando_def)[0]
                rando_def = rando_def[0].lower() + rando_def[1:]
                rando_def = re.sub("(\s)(she|he\/she|she\/he|he)(\s)", "\\1they\\3", rando_def)
                return rando_def
        except:
                print(rando_word, "something went wrong!")
                # if we can't make a valid tweet, we will just choose a different word
                # and try again

def generate_tweet_text():
    """
    Call make_german_word_from_data() and fetch_rando_definition(), stick them together
    using one of several pre-defined sentence patterns, then return complete sentence
    """

    sentence_patterns_def_first = ["The German word for %s is %s.",
                                    "In German, %s is called %s.",
                                    "Did you know the Germans have a word for %s? It's %s.",
                                    "I think it's kind of poetic that the German word for %s is %s.",
                                    "In German, you would call %s a %s.",
                                    "Germans call %s a %s.",
                                    'When German people talk about %s, they say "%s."'
                                    ]
    sentence_patterns_german_first = ["The German word %s means %s.",
                                      "%s is the German word for %s.",
                                      "Today's German lesson: When you say %s, it means %s."
                                      ]

    while True:
        gw = make_german_word_from_data("1.txt", "2.txt", "3.txt")
        rando_def = fetch_rando_definition()
        # randomly select which type of sentence pattern to use
        c = random.randint(0, 1)
        if c == 0:
            s = random.choice(sentence_patterns_def_first)
            # insert German word and random word definition into the sentence
            output = s % (rando_def.strip(), gw.strip())
        else:
            s = random.choice(sentence_patterns_german_first)
            output = s % (gw.strip(), rando_def.strip())

        # don't return if it's untweetable
        if len(output) <= 140:
            return output

def tweet_it(debug):
    """
    Call generate_tweet_text() and post result to Twitter. If debug is set to True,
    the result will not be tweeted, only printed.
    """
    status = generate_tweet_text()
    api = login()
    try:
        if debug:
            print(status)
        else:
            api.update_status(status=status)
            print(status)
    except:
        # if something goes wrong, the bot sends me a Direct Message with the traceback
        error_msg = traceback.format_exc().split("\n", 1)[1][-130:]
        api.send_direct_message(screen_name = owner, text = error_msg + " " + time.strftime("%H:%M:%S"))

debug = True
tweet_it(debug)