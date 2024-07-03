import praw
import os
from get_urls import reddit


# Read comment URLs from file
def read_existing_data(filename):
    data = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                author, count = eval(line.strip())
                data[author] = count
    return data
with open('reszta.txt', 'r', encoding='utf-8') as f:
    all_urls = [line.strip() for line in f]

# Initialize counters
comment_counter = read_existing_data('komentarze3.txt')
post_counter = read_existing_data('posty3.txt')
flair_counter = read_existing_data('flary3.txt')
processed_urls = set()
# Iterate through comment URLs
for i in range (len(all_urls)):
    print(900-i)
    try:
        url = all_urls[i]
        # Get the submission object
        submission = reddit.submission(url=f"https://www.reddit.com{url}")

        author = getattr(submission.author, 'name', '[deleted]')
        flara = submission.link_flair_text
        if flara in flair_counter.keys(): flair_counter[flara]+=1
        else: flair_counter[flara] = 1
        if author in post_counter.keys():
            post_counter[author] += 1
        else:
            post_counter[author] = 1

        # Iterate over comments in the submission
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            author = getattr(comment.author, 'name', '[deleted]')
            if author in comment_counter.keys():
                comment_counter[author] += 1
            else:
                comment_counter[author] = 1
        processed_urls.add(url)

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

comment_counter = sorted({(author, count) for author, count in comment_counter.items()}, key=lambda x: x[1], reverse=True)
post_counter = sorted({(author, count) for author, count in post_counter.items()}, key=lambda x: x[1], reverse=True)
flair_counter = sorted({(author, count) for author, count in flair_counter.items()}, key=lambda x: x[1], reverse=True)
with open('komentarze3.txt', 'w', encoding='utf-8') as f:
    for komentarz in comment_counter:
        f.write(str(komentarz) + '\n')
with open('posty3.txt', 'w', encoding='utf-8') as f:
    for post in post_counter:
        f.write(str(post) + '\n')
with open('flary3.txt', 'w', encoding='utf-8') as f:
    for flair in flair_counter:
        f.write(str(flair) + '\n')
unprocessed_urls = [url for url in all_urls if url not in processed_urls]
with open('reszta.txt', 'w', encoding='utf-8') as f:
    for url in unprocessed_urls:
        f.write(str(url) + '\n')