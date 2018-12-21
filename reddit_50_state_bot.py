import os
import time
import random
import requests
import praw
from bs4 import BeautifulSoup

SUBREDDIT = 'videos'   # For Multiple Subreddits: 'subreddit+subreddit+...+subreddit'
MINUTES_TO_SLEEP = 30

r = requests.get('https://www.50states.com/facts/')

soup = BeautifulSoup(r.text, 'html.parser')
base_url = soup.find('base')['href'] # https://www.50states.com/facts/
base_url = base_url.replace('/facts/','')

state_dict = {} # cache 'key':'value' as 'state_name':'state_url'

all_states = soup.find_all('a', attrs={'class':'displayBlock rounded stateLink orangeHover'})

for state in all_states:
    state_name = state['title'].lower()
    state_url = state['href']
    complete_url = base_url + state_url
    state_dict[state_name] = complete_url

# change dictionary key for washington state from 'washington' to 'washington '
# to fix some bugs
state_dict['washington '] = state_dict['washington']
del state_dict['washington']

# Create reddit client
reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET',
                     password='CLIENT_PASSWORD',
                     user_agent='CLIENT_USER_AGENT',
                     username='REDDIT_USERNAME')
print("**** LOGGED IN ****\n")

# Comments_replied is a list of user comment id's that have already been replied
# to. If a text file containing the list does not exist, create an empty list,
# else read the list from the text file that contains previous comments that have
# been replied to.
if not os.path.isfile('Comments_Replied_To.txt'):
    comments_replied = []
else:
    with open('Comments_Replied_To.txt', 'r') as f:
        comments_replied = f.read()
        comments_replied = comments_replied.split(',')


if __name__ == '__main__':
    while True:
        print(f'====> Running bot...on r/{SUBREDDIT}')

        for state in state_dict.keys():
            print('Searching for \'' + state + '\'')

            # scan first 100 new comments in specified subreddits
            for comment in reddit.subreddit(SUBREDDIT).comments(limit=100):

                # search for state name in comment, if the bot has not already replied
                # to this comment, and this comment is from any user beside the bot itself
                # send a reply
                if state in comment.body.lower() and comment.id not in comments_replied and comment.author != reddit.user.me():

                    try:
                        r = requests.get(state_dict[state])
                        soup = BeautifulSoup(r.text, 'html.parser')

                        fact_list = soup.find_all('ol')
                        state_facts = fact_list[0].find_all('li')
                        # randomly select a fact from first 12 on fact list
                        fact = state_facts[random.randrange(12)].text
                        reply = f'An interesting fact about {state.capitalize()} is that ' + fact

                        print('\nSubreddit: ', comment.subreddit.display_name)
                        print('\nAuthor:    ', comment.author.name)
                        print('\nComment:   ', comment.body)
                        print('\nReply:     ', reply)
                        print('\n','*'*30)
                         # Reply to user
                        comment.reply(reply)
                        # update list with additional comment id
                        comments_replied.append(comment.id)
                        with open('Comments_Replied_To.txt', 'a') as f:
                            f.write(comment.id + ',')

                    except Exception as e:
                        print(str(e))

        # sleep for specified time, then repeat
        print(f'\n----- End, Sleeping {MINUTES_TO_SLEEP} Minutes\n')
        print('='*60)
        print('='*60, '\n')
        time.sleep(MINUTES_TO_SLEEP * 60)
