from numpy import genfromtxt
from gensim import corpora, models, similarities
import re
from nltk.corpus import stopwords
import logging, gensim, bz2
import pickle 
import sys

print "getting stop words.."
stops = set(stopwords.words("english"))
stops.add('www')
stops.add('com')
stops.add('http')
stops.add('ww')
stops.add('https')



def cleanup_text(text):
    
    #1. remove punctuation 
    nopunc = re.sub("[^a-zA-Z]"," ", text) 
    #2. split to words
    words = nopunc.split()
    #3. remove single leter words and very long words
    words = [w for w in words if (len(w)>1 and len(w)<20)]
    #4. remove stop words
    meaningful_words = [w for w in words if not w in stops] 
    #5.and return. 
    return meaningful_words

#open data file for comments. Skip header
print "opening file.."
file_lines = open('../data/subs.data','rd').readlines()[1:]

# make list of subreddits and comments. Use |:| as delim. Fix comment lines. Clean up comments. 
subreddit = []
comment = []
for line in file_lines:
    if line.find('|:|')>0:
        subreddit.append(line.split('|:|')[0])
        comment.append(line.split('|:|')[1].rstrip().lower()+ " " + line.split('|:|')[2].rstrip().lower())
    else:
        comment[-1] += (" " + line).rstrip().lower()

print "cleaning doc.."
cleaned_comment = []
for com in comment:
    cleaned_comment.append(cleanup_text(com))

#remove words that only occur once
print "removing stop words"
all_tokens = sum(cleaned_comment, [])
token_set = set(all_tokens)
tokens_once = set(word for word in token_set if all_tokens.count(word) == 1)
comment_tokens = [[word for word in text if word not in tokens_once] for text in cleaned_comment]
pickle.dump(comment_tokens, open('../data/comment_tokens.pkl','wd'))

print "making dict"
dictionary = corpora.Dictionary(comment_tokens)
dictionary.save('../model/comments_'+sys.argv[1]+'.dict') # store the dictionary, for future reference
print(dictionary)

print "making corpus"
corpus = [dictionary.doc2bow(text) for text in comment_tokens]
corpora.MmCorpus.serialize('../model/comments'+sys.argv[1]+'.mm', corpus)

print "loading corpus"
mm = corpora.MmCorpus('../model/comments'+sys.argv[1]+'.mm')
print mm

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#print "training LDA model"
#lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=int(sys.argv[1]), update_every=1, chunksize=10000, passes=5)
#lda.print_topics()

#save_name = '../model/lda_model_' + sys.argv[1] + '.pkl'
#print 'saving model ', save_name
#pickle.dump(lda, open(save_name, 'wd'))




