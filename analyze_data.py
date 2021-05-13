"""In this file we will visualize the data and answer some
   questions about climate change
   The dataset we are using is a collection of 7000 tweets,
   with information about sentiment score of the tweet,all
   the hashtags associated with the tweets,number of likes
   the tweet got,number of times the tweet was retweeted,
   date of creation,username of the user,users followers
   count,and location of the user.
   The dataset is made by us, using the twitter API, to
   extract tweets on 6 hashtags on climate change. The
   sentiments were calculated using dataset of words
   called the Sentiword dataset, which contains positive
   and negative words, with their corresponding scores.
   References:
   - https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
   """
import operator
from typing import Dict
from datetime import datetime
import matplotlib.pyplot as plt
from data_manager import Dataset


def load_data(filename: str) -> Dataset:
    """Use data handler library to extract data from our dataset
    @param filename: path for the dataset
    @return: dataset as a list of list
    """
    return Dataset(filepath=filename,
                   types=[str, float, str, list, int, int, datetime, str, int, str])


def grp_by_days(date: datetime) -> float:
    """This is a filter function for grouping the data by dates
    :param date: the datetime object
    :return: the day of the datetime object
    """
    return date.day


def plot_sentiments(filepath: str) -> None:
    """Use matplotlib.pyplot to plot a scatterplot with lines joining the points
    @param filepath: path for the dataset
    @return: The function just plots a graph
    """
    data = load_data(filepath)

    x, y = data.calculate_average(6, 1, grp_by_days)

    date, value = x.pop(), y.pop()

    list.insert(x, 0, date)
    list.insert(y, 0, value)

    plt.plot(x, y, marker='o')
    plt.show()


def word_count(string: str) -> Dict[str, int]:
    """Count the number of times all the words are occurring in the string
    and return a dict with each word mapped to its count
    @param string: The string for which we want word count
    @return: dict mapping word to its count
    """
    tags = ['#climatechange',
            '#climatechangeisreal',
            '#actonclimate'
            '#globalwarming',
            '#climatechangehoax',
            '#climatedeniers',
            '#climatechangeisfalse',
            '#globalwarminghoax',
            '#climatechangenotreal']

    words = {}
    text = string. \
        replace('.', ''). \
        replace('"', ''). \
        replace(',', ''). \
        replace('-', ''). \
        replace('_', ''). \
        replace('#', ''). \
        replace('?', ''). \
        replace('@', '').lower()

    for element in text.split():
        if len(element) > 6 and all(element not in hashtag for hashtag in tags):
            if element in words:
                words[element] += 1
            else:
                words[element] = 1

    return words


def plot_top_10(filepath: str) -> None:
    """Plot a count-plot for the highest occurring words in the tweets
    @param filepath: path to the dataset
    """
    data = Dataset(filepath)
    text = ''

    for tweet in data.get():
        text += tweet[0]

    words = word_count(text)

    sorted_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)[:11]

    plt.bar([word[0] for word in sorted_words],
            [word[1] for word in sorted_words])
    plt.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['datetime',
                          'matplotlib.pyplot',
                          'data_manager',
                          'typing',
                          'operator'],
        'allowed-io': [],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
