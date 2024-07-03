import arrow
import praw
from datetime import datetime
import pytz
from get_urls import reddit


subreddit_name = 'Polska'
existing_urls = set()
with open(f'{subreddit_name}_thread_comment_urls_lipiec.txt', 'r', encoding='utf-8') as existing_file:
    for line in existing_file:
        existing_urls.add(line.strip())

early_date =datetime(2100, 10, 20, 0, 0, 0)
early_date = pytz.utc.localize(early_date)
for line in existing_urls:
    post_url = f'https://www.reddit.com{line}'
    submission = reddit.submission(url=post_url)
    post_date = arrow.get(submission.created_utc).datetime
    if post_date<early_date: early_date = post_date
    print(early_date)


#post_url = 'https://www.reddit.com/r/Polska/comments/1d0h3ej/jak_schudnąć/'
#submission = reddit.submission(url=post_url)
#post_date = arrow.get(submission.created_utc).datetime

#print(post_date)