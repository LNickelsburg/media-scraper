import praw
import pandas as pd

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
    subreddit = reddit_read_only.subreddit(name)
    for post in subreddit.top(limit=100):

        # collect comments
        post.comments.replace_more(limit=100)
        comments = []
        for comment in post.comments.list():
            comments.append(comment.body)
        
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
        
df = pd.DataFrame(all_posts)
df.to_csv('reddit_data.csv', index=False, encoding='utf-8')