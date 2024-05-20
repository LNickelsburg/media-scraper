import praw # type: ignore
import csv


'''run this separately for each subreddit so u dont get rate limited'''

reddit_read_only = praw.Reddit(client_id = 'Dwr17XS-Rc4T4WETNJF9_w',
                               client_secret = 'kRmJ1cu1rtjYpe3J2YL02pQANNb6zQ',
                               user_agent = 'web:osint_scraper:v1 (by u/notaflightlessbird)')

'''subreddit_list = ['gazainvasionfootage',
                    'israelpalestine', 
                    'israelwarvideoreport', 
                    'israel_palestine',
                    'osint',
                    'palestine', 
                    '2ndyomkippurwar']
'''

subreddits_dict = {"Display Name": [], "Title": [], 
                   "Description": [], "Subscribers": [], 
                   "Posts": []}

name = '2ndyomkippurwar'
subreddit = reddit_read_only.subreddit(name)
subreddits_dict["Display Name"].append(subreddit.display_name)
subreddits_dict["Title"].append(subreddit.title)
subreddits_dict["Description"].append(subreddit.description)
subreddits_dict["Subscribers"].append(subreddit.subscribers)

subreddit_posts = []
for post in subreddit.top(limit=100):
    subreddit_posts.append((post.url, post.title, post.selftext, post.score, post.num_comments))


subreddits_dict["Posts"].append(subreddit_posts)

filename = "./posts/" + name + "_posts.txt"
file = open(filename, "w", encoding='utf-8')
for post_list in subreddits_dict["Posts"]:
    for post in post_list:
        file.write(str(post) + "\n")