# Deutsch_Falsch
Twitterbot that generates orthographically plausible German words with semantically plausible English definitions. See [https://twitter.com/Deutsch_Falsch] (@Deutsch_Falsch) for sample output.

## How it works
The German words are generated using a trigram model that was trained on actual German nouns. The files `1.txt`, `2.txt` and `3.txt` contain all unigrams, bigrams and trigrams from my noun list with their frequency. The new words are randomly generated so that they have the same character and n-gram distribution as the actual German words.
The English definitions are taken from Wordnik definitions that are collected randomly by looking up English nouns from a word list.

## Why I made it
German is a strange language. I'm currently focusing on making twitterbots that have something to do with German. At the same time, I wanted to do a project that people who don't speak German can still appreciate. That's why the language of the tweets is English while their topic is the German language.
Also, I wanted to ridicule the "There must be a German word for `_______` " meme.

## Apologies
I'm sorry my bot teaches you wrong German words. Many tweets of the bot are actually being retweeted by "Long German Words" accounts. I hope nobody actually believes what they read here! If you have any specific complaints, you can reach me via GitHub or twitter.