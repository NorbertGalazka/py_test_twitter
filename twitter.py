import os.path
import re
import requests
import urljoin
import json


URL_API = 'https://api.github.com/users'


class Twitter:
    version = 1.0

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username

    def tweet_messages(self):
        return [tweet['message'] for tweet in self._tweets]

    def delete_backend(self):
        if self.backend:
            os.remove(self.backend)

    def tweets(self):
        if self._tweets:
            return self._tweets
        else:
            if os.path.exists(self.backend):
                with open(self.backend) as f:
                    return json.loads(f.read())
            else:
                return []

    def get_user_avatar(self):
        if not self.username:
            return None

        url = urljoin.url_path_join(URL_API, self.username)
        res = requests.get(url)
        return res.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception('Message is to long')
        self._tweets.append({'message': message, 'avatar': self.get_user_avatar()})
        if self.backend:
            with open(self.backend, 'w+') as twitter_file:
                twitter_file.write(json.dumps(self._tweets))

    @staticmethod
    def find_hastags(message):
        return re.findall("#(\\w+)", message)


t2 = Twitter(backend='xd.txt', username="Maciek")
print(t2.tweets())