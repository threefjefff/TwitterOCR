import requests
from lxml import html
from reddit import RedditReader
import ocr
from sqlite_store import SqliteStore
from PIL import Image

store = SqliteStore()
for submission in RedditReader().get_posts('scottishpeopletwitter'):

    store.save_reddit_post(submission.permalink, submission.url, submission.title)
    resp =requests.get(submission.url, stream=True)
    if 'text/html' in resp.headers['content-type']:
        print("'%s' isn't a supported source" % submission.url)
        # tree = html.fromstring(resp.content)
        # imgurl = tree.xpath('//img[@class="post-image-placeholder"]/@src')
        # resp = requests.get(imgurl, stream=True)
    try:
        resp.raw.decode_content = True
        img = Image.open(resp.raw)
        txt = ocr.text_from_image(img)
        if ocr.twitter_handle(txt) is not None:
            print(ocr.multiline_cleanup(txt))
            store.save_tweet(submission.permalink,txt, submission.url,resp.headers['content-type'], img.tobytes())
    except OSError:
        print("Exception: '%s' isn't an image" % submission.url)