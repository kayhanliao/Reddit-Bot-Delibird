import praw
from time import sleep
import time

keywords = ['M6-A','M6-C','M6-B','macropad','Dolch']

alertedPosts = []


start_time = time.time()

file = open('delibird_info.txt','r')
user_info = file.read().split('\n')
file.close()

reddit = praw.Reddit(
    client_id=user_info[0],
    client_secret=user_info[1],
    user_agent=user_info[2],
    username=user_info[3],
    password=user_info[4]
 )

print('praw')

mm = reddit.subreddit("mechmarket")

def sendMessage(word,title,link,author):
    superString = 'Found ' + str(word) + ' in post by ' + str(author)  + ' Title: ' +str(title) + '\n' + 'link: ' + str(link)
    me = reddit.redditor('kayhanliao')
    me.message(subject = 'Found ' + str(word) + ' in post by ' + str(author), message = superString)


def main():
    try:
        for submission in mm.stream.submissions():
            if submission.created_utc < start_time:
                continue
            if submission.id in alertedPosts:
                continue
            title, text, link, author = submission.title, submission.selftext, submission.url, submission.author
            flair = submission.link_flair_text
            for word in keywords:
                variations = [word,word.upper(), word.lower()]
                for key in variations:
                    if key in title or key in text:
                        sendMessage(key,title,link,author)
                        alertedPosts.append(submission.id)
                        break
    except Exception as e:
        print(str(e))
        sleep(60)
        main()
if __name__ == '__main__':
    main()
