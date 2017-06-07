import praw


class RedditReader:
    """"Read posts from a specified subreddit. requires praw.ini"""

    def __init__(self):
        self.__reddit = praw.Reddit('threefjefff')
        self.username = self.__reddit.user.me()
        print("Logged in as '%s'" % self.username)

    def get_posts(self, subreddit):
        return self.__reddit.subreddit(subreddit).hot()
