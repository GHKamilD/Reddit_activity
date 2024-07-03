import praw
import os

# Initialize Reddit instance
reddit = praw.Reddit(client_id='insert_id',
                     client_secret='insert_secret',
                     user_agent='insert_agent')
# Specify the subreddit name
subreddit_name = 'Polska'

existing_urls = set()
if os.path.exists(f'{subreddit_name}_thread_comment_urls_lipiec.txt'):
    with open(f'{subreddit_name}_thread_comment_urls_lipiec.txt', 'r', encoding='utf-8') as existing_file:
        for line in existing_file:
            existing_urls.add(line.strip())


print(existing_urls)
# Get the subreddit instance
subreddit = reddit.subreddit(subreddit_name)

# Create a list to store thread URLs
new_thread_urls = set()

# Iterate through the new submissions
for submission in subreddit.new(limit=None):
    # Get the permalink for the submission (leads to the comments section)
    thread_url = submission.permalink
    new_thread_urls.add(thread_url)



all_urls = existing_urls.union(new_thread_urls)

print(new_thread_urls==existing_urls)

# Save the URLs to a text file
with open(f'{subreddit_name}_thread_comment_urls_lipiec.txt', 'w', encoding='utf-8') as f:
    for url in all_urls:
        f.write(url + '\n')

print(f"Thread comment URLs from r/{subreddit_name} saved to {subreddit_name}_thread_comment_urls.txt")