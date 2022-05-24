# -*- coding: utf-8 -*-
"""
Created on Fri May 20 07:36:10 2022

@author: phsta
"""

import praw
from psaw import PushshiftAPI
import pandas as pd
import numpy as np
import os
import datetime as dt
import re
import matplotlib.pyplot as plt

# set up is in a different, non-tracked, local file for confidentiality reasons 

#api = PushshiftAPI(reddit)


"""
# This code uses the PushshiftAPI because that API allows
# users to take top posts within a time period
# That is part two of this project, so I have
# code it out for now.
start_epoch=int(dt.datetime(2017, 1, 1).timestamp())

list(api.search_submissions(after=start_epoch,
                            subreddit='politics',
                            filter=['url','author', 'title', 'subreddit'],
                            limit=10))
"""

# This is a csv with a list of the non-local political subreddits in 2021
# with over 10k users
pol_reddits = pd.read_csv("pol_subreddits.csv")

sources_df = pd.DataFrame()

count = 0
lim = 500
# i'm writing this so that if it breaks, I don't iterate the count,
# instead, I run the code inside the final else statement
# and then re-run it for the next section. Actually, no
# i want to iterate count after I run it so that in a neutral state
# i run it with count = 0. Plus it's better actually run it over once than
# mess up.
for subname in pol_reddits['subreddit'][count:]:
    # initialize an empty array that will hold the names
    cf_list = []
    for submission in reddit.subreddit(subname).top(limit=lim, time_filter="year"):
        # grab the url for the submission
        sub_url = reddit.submission(submission).url
        # find the main portion of the url. This seems to be the easiest way
        # given the occassional lack of www. and the variety of
        # endings (.org, .com, .co.uk etc).
        if (re.search('//(.+?)/', sub_url) != None):
            sub_url = re.search('//(.+?)/', sub_url).group(1)

        # add it to the list.
        cf_list = cf_list + [sub_url]
    if count == 0:
        sources_df = pd.DataFrame({subname: cf_list})
    else:
        new_col = pd.DataFrame({subname: cf_list})
        sources_df = pd.concat([sources_df, new_col], axis=1)
    count += 1

sources_df.to_csv("subreddits_sources.csv")


"""
I think the first thing I actually want to do is see
whether I have enough datapoints to actually capture
sources per place. I think I can do this with a bar chart
per subreddit maybe. But there should be a better way to do this.
"""

subname = "politics"
num_inc = 10
sub_group = sources_df.groupby(by=subname).size().sort_values(ascending=False)
num_other = sum(sub_group[num_inc:, ])

sub_group = sub_group[:num_inc, ]
sub_group['other'] = num_other

bar_names = list(sub_group.index)

plt.bar(bar_names, sub_group)

"""
I kind of want to try a basic cluster analysis or something
to identify the different subreddits by source commonality.
It would be fun to try and display this, but I'm not sure how
I would...

I think I could make a dataset where the rows are subreddits, the columns are
the unique named urls, and the values are counts of each url for each subreddit.
"""
cluster_df_beg = sources_df.melt()

all_url = cluster_df_beg['value'].unique()
all_subreddits = cluster_df_beg['variable'].unique()

url_counts = cluster_df_beg.groupby(["variable", "value"], as_index = False)

url_counts = url_counts.size()

cluster_df = url_counts.pivot(index = "variable", columns = "value").fillna(0)


"""
I want to try a k-means clustering algorithm. I'm a bit wary that it won't
work very well with a sparse dataset like this one, but I figure I'll try
and see what happens. This is for tomorrow. Plus I think I need to
do some kind of dimension reduction before given the curse of dimensionality. 
Maybe PCA but maybe a different thing...
"""
