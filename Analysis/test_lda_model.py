import pickle
import gensim
import sys
from gensim import corpora, models, similarities
import logging, gensim

load_file_name = '../model/lda_model_'+sys.argv[1]+'.pkl'
print "loading file: ", load_file_name

load_file = open(load_file_name, 'rd')
lda = pickle.load(load_file)
load_file.close()

print "opening comments file.."
file_lines = open('../data/comments.data','rd').readlines()[1:]

# make list of subreddits and comments. Use |:| as delim. Fix comment lines. Clean up comments. 
subreddit = []
comment = []
for line in file_lines:
    if line.find('|:|')>0:
        subreddit.append(line.split('|:|')[0])
        comment.append(line.split('|:|')[1].rstrip().lower())
    else:
        comment[-1] += (" " + line).rstrip().lower()

#load_tokens = open('../data/comment_tokens.pkl','rd')
#comment_tokens = pickle.load(load_tokens)
#load_tokens.close()

f_name = sys.argv[1]
n_topics = int(sys.argv[2])

print "loading corpus"
mm = corpora.MmCorpus('../model/comments'+f_name+'.mm')

doc_lda = lda[mm]

sub_set = set(subreddit[:10000])

#calculate the average distributions for a given subreddit 
#first initailize 
lda_dist = dict()
count_dict = dict()
for sub in sub_set:
	lda_dist[sub] = [0.]*n_topics
	count_dict[sub] = 0.0

for sub, dist in zip(subreddit, doc_lda):
	count_dict[sub] += 1.
	for p in dist:
		lda_dist[sub][p[0]] += p[1]

for sub in lda_dist:
	for i in range(n_topics):
		lda_dist[sub][i] *=1./max(count_dict[sub],1)

import operator

for i in range(n_topics):
	for sub in lda_dist:
		index, value = max(enumerate(lda_dist[sub]), key=operator.itemgetter(1))
		if index == i:
			print "index: ", i,  " subreddit: ", sub, " value: ", value
			#del lda_dist[sub]


#for sub, doc in zip(subreddit, doc_lda):
	#print "subreddit: ", sub, " | ", doc
