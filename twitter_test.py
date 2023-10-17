import pytest

from twitter import Twitter


@pytest.fixture(params=[None, 'test.txt'], name='twitter')
def fixture_twitter(request):
    twitter = Twitter(backend=request.param)
    return twitter


def test_twitter_initialization(twitter):
    assert twitter


def test_twitter_message(twitter):
    twitter.tweet('test message')
    assert twitter.tweet_messages() == ['test message']
    twitter.delete_backend()


def test_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet('test' * 41)
    assert twitter.tweet_messages() == []


@pytest.mark.parametrize("message, expected",
                         (("Test #first message", ["first"]),
                          ("Test #FIRST message", ["FIRST"]),
                          ("#first test message", ['first']),
                          ("Test the message #first and #second", ['first', 'second'])
                          ))
def test_tweet_with_hashtag(message, expected, twitter):
    assert twitter.find_hastags(message) == expected
