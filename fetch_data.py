
def read_vocab():
    """
    Read a German word list and write unigram, bigram and trigram counts from that
    list into separate files.
    """
    unigrams = {}
    bigrams = {}
    trigrams = {}

    nouns = set()
    lexicon = open("D:/Korpora/german.dic", "r", encoding="utf8")
    for line in lexicon.readlines():
        if len(line) > 0:
            # German words that start with a capital letter are nouns
            if line[0].isupper():
                nouns.add(line.strip())

    for w in nouns:
        for i in range(len(w)-1):
            if i == 0:  # collect only word-initial unigrams
                if w[i] in unigrams:
                    unigrams[w[i]] += 1
                else:
                    unigrams[w[i]] = 1

                b = w[i:i+2]    # collect only word-initial bigrams
                if b in bigrams:
                    bigrams[b] += 1
                else:
                    bigrams[b] = 1#

            if i <= len(w)-3:
                t = w[i:i+3]
                if t in trigrams:
                    trigrams[t] += 1
                else:
                    trigrams[t] = 1

            # at some point, we don't have 3 characters left in the word. Then we
            # append a word-boundary marker to the final bigram (making it a trigram)
            else:
                t = w[i:]+"#"
                if t in trigrams:
                    trigrams[t] += 1
                else:
                    trigrams[t] = 1

    # write dictionary contents to files
    uni_file = open("1.txt", "w", encoding="utf8")
    for key in unigrams:
        uni_file.write(key + "\t" + str(unigrams[key]) + "\n")
    uni_file.close()
    bi_file = open("2.txt", "w", encoding="utf8")
    for key in bigrams:
        bi_file.write(key + "\t" + str(bigrams[key]) + "\n")
    bi_file.close()
    tri_file = open("3.txt", "w", encoding="utf8")
    for key in trigrams:
        tri_file.write(key + "\t" + str(trigrams[key]) + "\n")
    tri_file.close()

    return

read_vocab()
