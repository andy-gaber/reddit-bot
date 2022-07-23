# reddit-bot

This program utilizes Python's HTML parser Beaustiful Soup, and Reddit's Python Reddit API Wrapper (PRAW).

The website https://www.50states.com/facts/ contains a list of all 50 states, each with a link to a separate page displaying between 10 to 50 facts of that particular state. Beautiful Soup is used to parse the list of states and their webpages, while a dictionary is then populated to map each state to its unique facts webpage. 

PRAW is used to create a Reddit client bot to crawl through the 100 newest comments in a subreddit (or subreddits) specified by the user. If a state is mentioned in a comment by a Reddit user, the dictionary is used to access that state's fact page, where a randomly selected fact will be taken and replied back to that user. 

Additionally, a list is created and used to store each comment's unique comment ID to prevent continually replying to the same comment. It is accessed and updated with each reply. The bot runs on an infinite loop and can be canceled at any time by the user.
