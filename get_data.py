"""
This file is used to extract data from the twitter api and
make the dataset we would work on to make conclusions and
analyze real world statistics.

References:
- https://www.programiz.com/python-programming/writing-csv-files
- https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/overview/tweet-object
- http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html
- http://docs.tweepy.org/en/v3.5.0/api.html#tweepy-api-twitter-api-wrapper
"""

import csv  # for storing the data
import tweepy  # for getting tweets


def search_for_query(max_items: int, path: str) -> None:
    """
    This function will get us the most recant <items> tweets on the hashtags we give the function in the form of
    a search query. Here we use the tweepy api to extract these tweets and write all these tweets on csv. We can
    extract many features out of the tweets like the its timestamp,the tweet, username, all the hashtags in that
    tweet, followers count of that user, location if mentioned and many more, but we would only extract a few of
    them.

    @param max_items: The maximum number of tweets we want starting from the most latest tweet
    @param path: path/name of the csv file
    @return: None

    Preconditions:
    - consumer_key is a valid twitter consumer key
    - consumer_key_secret is a valid twitter secret consumer key
    - access_token is a valid twitter access token
    - access_token_secret is a valid twitter secret access token
    - items > 0
    """
    consumer_key = 'oYpwnrbV5Y9ALcdwdQhRkSsLR'
    consumer_key_secret = 'HHF5PMHys5oFfUeqFgKJIZRwkq0vyWl0mKyBaU3zIFyAV2GCMO'
    access_token = '1323930219263135745-exoYkKfak1aosBU0eVDWTzxW1AFAjo'
    access_token_secret = 'ilX1qD8VROXJh9CG7ow5OPJG2wnPXxpmuWTlXYAAHAyVF'

    tags = ['#climatechange',
            '#climatechangeisreal',
            '#actonclimate'
            '#globalwarming',
            '#climatechangehoax',
            '#climatedeniers',
            '#climatechangeisfalse',
            '#globalwarminghoax',
            '#climatechangenotreal']

    # using tweepy to authenticate for accessing twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initializing API used to do access all the function in the library
    api = tweepy.API(auth, wait_on_rate_limit=True)

    with open(path, 'w', newline='') as file:
        write = csv.writer(file)

        # add column names, as the first row of the dataset we would create
        # these are all the features we would extract from the tweets
        write.writerow(
            ['tweet_text',  # text of the tweet
             'all_hashtags',  # list of all the hashtags in the tweet
             'favorite_count',  # number of likes to the tweet
             'retweet_count',  # number of times the tweet was retweeted
             'created_at',  # date and time of creation
             'username',  # username of the person who tweeted the tweet
             'followers_count',  # number of followers the user has
             'location'])  # the location of the user

        # request the data the twitter api

        # we would be using api.search function to get the tweets which takes in parameters like the search query,
        # page from which we want to extract (1 <= page <= 1500). A single page has only about 100 tweets and if we
        # want more tweets we have to call the function multiple times on different pages. Thus we would use
        # "tweppy.Coursor" function in which we could specify the number of tweets we want and it would automatically
        # change the page.

        for hashtag in tags:
            # extracting tweets in a list.
            # tweets here is a list of tweet objects which contains all the information about a tweet
            tweets = tweepy.Cursor(api.search, q=hashtag + ' -filter:retweets', lang='en', tweet_mode='extended').items(
                max_items)

            # extracting out the features we want from the tweets and writing them into csv file
            for tweet in tweets:
                write.writerow([
                    tweet.full_text.replace('\n', ' '),  # the text of the tweet in one line rather than multiple lines
                    tweet.entities.get('hashtags'),  # list of dicts where each dict contains info about a sing hashtag
                    tweet.favorite_count,  # number of likes on the tweet
                    tweet.retweet_count,  # number of times this tweet has been retweeted
                    tweet.created_at,  # the date and time of creation
                    tweet.user.screen_name,  # username of the user
                    tweet.user.followers_count,  # number of followers the user has
                    tweet.user.location  # location of the user
                ])


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tweepy',
                          'csv',
                          'typing'],
        'allowed-io': ['search_for_query'],
        'max-line-length': 150,
        'disable': ['R1705', 'C0200']
    })
