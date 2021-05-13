"""
This file is used to create a dataset similar to
the tweeter data we already have but with an extra
column for the sentiment score of the tweet, based
on dataset of collection of words we have
"""

# import libraries
from datetime import datetime
from typing import Dict, Tuple
import csv
import ast


def add_sentiments_to_data(filename: str, words_list: str) -> None:
    """ The function reads the dataset with all the tweets and sentiment score
    to the dataset to produce a new dataset.

    @param filename: the path of the dataset with all the tweets
    @param words_list: the path for the dataset with words for calculating sentiment score
    @return: None

    Preconditions:
    - filename is a valid path
    """

    # getting the words dictionary for calculating sentiment score
    words = extract_words(words_list)

    # extracting the tweet text out of the data
    with open(filename, 'r') as input_file:
        with open('datasets/twitter/climate-change-sentiment.csv', 'w') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            next(reader)

            reader = list(reader)

            writer.writerow(['tweet_text',  # text of the tweet
                             'senti-score',  # sentiment score of the tweet
                             'senti-type',  # neutral, positive or negative
                             'all_hashtags',  # list of all the hashtags in the tweet
                             'favorite_count',  # number of likes to the tweet
                             'retweet_count',  # number of times the tweet was retweeted
                             'created_at',  # date and time of creation
                             'username',  # username of the person who tweeted the tweet
                             'followers_count',  # number of followers the user has
                             'location'])  # the location of the user

            for row in reader:
                score, tag = analyze_sentiments(row[0], words)
                writer.writerow([row[0],
                                 score,
                                 tag,
                                 ast.literal_eval(row[1]),
                                 int(row[2]),
                                 int(row[3]),
                                 datetime.fromisoformat(row[4]),
                                 row[5],
                                 int(row[6]),
                                 row[7]])


def extract_words(filename: str) -> Dict[str, float]:
    """ The function reads the dataset with all the positive and negative words
    and returns a list of dicts with all the words mapped to a score of -1 to 1
    where -1 is very negative and 1 is very positive word. if a word has a score
    of 0 then the word is neutral.

    The words in the data are in the form of lemma, that is word#type where type
    can be adjectives, nouns, verbs and adverbs. we will remove the type and only
    keep the word.

    Also words have _ and - instead of space, but while writing tweets we usually
    do not use - or _, instead we us space, thus we would replace all - and _ to
    space.

    @param filename: the path of the dataset with all the words and their cores
    @return: a dict mapping word to its score

    Preconditions:
    - filename is a valid path
    """

    # extracting the file
    with open(filename) as file:
        reader = []

        for line in file.read().split('\n'):
            if line != '' and line[0] != '#':
                reader.append(line)

        words_so_far = {}  # ACCUMULATOR: stores the return data

        for line in reader:
            lemma, pos = line.split()

            word = lemma.split('#')[0].replace('-', ' ').replace('_', ' ')  # modifying the word
            score = float(pos)  # converting score into numeric data type

            words_so_far[word] = score  # adding word and its score to return dict

        return words_so_far


def analyze_sentiments(tweet_txt: str, words_list: Dict[str, float]) -> Tuple[float, str]:
    """ Returns a sentiment score for the tweet by adding up the score of all
    the words it contains which are in the words list.

    The score only depends on the words with a magnitude higher that 0, thus we
    would remove words with score 0. This would help in increasing the speed of the
    loop.

    @param tweet_txt: The tweet for which we want to analyze sentiments
    @param words_list: the list of words with their sentiment scores
    @return: a sentiment score for the tweet
    """

    # remove neutral words from the list as they don't impact the sentiments
    refined_list = {}

    for word in words_list:
        if words_list[word] != 0:
            refined_list[word] = words_list[word]

    # our words in the refined_list are only lowe-case  so we have to covert
    # the tweet into all lower-case.
    text = str.lower(tweet_txt)

    score_so_far = 0.0  # ACCUMULATOR: stores the sentiment score
    tag = 'neutral'

    for word in text.split():
        if word in refined_list:
            score_so_far += refined_list[word]

    if score_so_far >= .5:
        tag = 'positive'
    elif score_so_far <= -.25:
        tag = 'negative'

    return (score_so_far, tag)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['datetime',
                          'csv',
                          'ast',
                          'typing'],
        'allowed-io': ['add_sentiments_to_data', 'extract_words'],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
