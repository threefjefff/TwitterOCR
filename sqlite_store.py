import sqlite3

def using(func):
    def using_wrapper(self, *args):
        conn = sqlite3.connect(self.db_name)
        func(self, conn.cursor(), *args)
        conn.close()
    return using_wrapper

class SqliteStore:
    def __init__(self, db = 'C:\\apps\\spt\\scottishpeopletwitter.db'):
        self.db_name = db

    @using
    def save_reddit_post(self, cursor, permalink, submission_link, title):
        cursor.execute('SELECT COUNT(*) FROM reddit_posts WHERE permalink = ?', (permalink,))
        if(cursor.fetchone() == 0):
            cursor.execute('INSERT INTO reddit_posts(permalink, submission_link, title) VALUES (?,?,?)',
                     (permalink,submission_link,title))
            cursor.commit()

    @using
    def save_tweet(self, cursor, permalink, text, img_link, img_mime, img ):
        cursor.execute('SELECT COUNT(*) FROM reddit_posts WHERE permalink = ?', (permalink,))
        if (cursor.fetchone() == 0):
            cursor.execute('INSERT INTO processed_tweets(reddit_post, scanned_text, image_href, image_mime, image) VALUES (?, ?, ?, ?, ?)',
                     (permalink,text,img_link,img_mime,img))
            cursor.commit()