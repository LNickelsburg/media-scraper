import praw
import pandas as pd
import time
from prawcore.exceptions import RequestException, ServerError, TooManyRequests

reddit_read_only = praw.Reddit(client_id = 'Dwr17XS-Rc4T4WETNJF9_w',
                               client_secret = 'kRmJ1cu1rtjYpe3J2YL02pQANNb6zQ',
                               user_agent = 'web:osint_scraper:v1 (by u/notaflightlessbird)')

subreddit_list = ['gazainvasionfootage',
                  'israelpalestine', 
                  'israelwarvideoreport', 
                  'israel_palestine',
                  'osint',
                  'palestine', 
                  '2ndyomkippurwar']

all_posts = []

for name in subreddit_list:
    print(f"Fetching posts from subreddit {name}...")
    try:
        subreddit = reddit_read_only.subreddit(name)
        post_counter = 0
        for post in subreddit.top(limit=10):
            post_counter += 1
            #print (f"Fetching post {post_counter} from subreddit {name}...")

            # collect comments
            comments = []
            if post.num_comments != 0:
                try:
                    post.comments.replace_more(limit=10)
                    comment_counter = 0
                    for comment in post.comments.list():
                        comment_counter += 1
                        #print(f"Fetching comment {comment_counter} from post {post_counter} in subreddit {name}...")
                        comments.append(comment.body)
                except (RequestException, ServerError, TooManyRequests) as exception:
                    print(f"Error: {exception}")
                    time.sleep(5)
            
            # add comments and post info to list
            all_posts.append({
                "subreddit": name,
                "url": post.url,
                "title": post.title,
                "selftext": post.selftext,
                "score": post.score,
                "id": post.id,
                "num_comments": post.num_comments,
                "comments": comments,
                "created": post.created
                })
            time.sleep(5)
    except TooManyRequests as exception:
        print(f"Rate limited: {exception}")
        print(f"Waiting for 10 seconds before moving on...")
        time.sleep(10)
        
df = pd.DataFrame(all_posts)
df.to_csv('reddit_data.csv', index=False, encoding='utf-8')