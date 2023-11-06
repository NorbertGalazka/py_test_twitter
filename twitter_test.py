import pytest
from unittest import mock
from twitter import Twitter
import requests


class ResponseGetMock:
    @staticmethod
    def json():
        return {'avatar_url': 'test'}


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture(params=[None, "Norbert"])
def username(request):
    return request.param


@pytest.fixture(params=[None, 'test.txt'], name='twitter1')
def fixture_twitter(request, username, monkeypatch):
    twitter = Twitter(backend=request.param, username=username)

    return twitter


def test_twitter_initialization(twitter1):
    assert twitter1


@mock.patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_message(avatar_mock, twitter1):
    twitter1.tweet('test message')
    assert twitter1.tweet_messages() == ['test message']
    twitter1.delete_backend()


def test_long_message(twitter1):
    with pytest.raises(Exception):
        twitter1.tweet('test' * 41)
    assert twitter1.tweet_messages() == []


@pytest.mark.parametrize("message, expected",
                         (("Test #first message", ["first"]),
                          ("Test #FIRST message", ["FIRST"]),
                          ("#first test message", ['first']),
                          ("Test the message #first and #second", ['first', 'second'])
                          ))
def test_tweet_with_hashtag(message, expected, twitter1):
    assert twitter1.find_hastags(message) == expected


@mock.patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter1):
    if not twitter1.username:
        pytest.skip()
    twitter1.tweet('Test message')
    assert twitter1.tweets() == [{'message': 'Test message',
                                  'avatar': 'test',
                                  'hashtags': []}]
    avatar_mock.assert_called()


@mock.patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hastag_mock(avatar_mock, twitter1):
    twitter1.find_hastags = mock.Mock()
    twitter1.find_hastags.return_value = 'first'
    twitter1.tweet('Test #second')
    assert twitter1._tweets[0]['hashtags'] == 'first'
    twitter1.find_hastags.assert_called()


def test_twitter_version_mock(twitter1):
    twitter1.version = mock.MagicMock()
    twitter1.version.__eq__.return_value = 2.0
    assert twitter1.version == 2.0


def test_twitter_version(twitter1):
    assert twitter1.version == twitter1.get_twitter_version
