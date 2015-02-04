import sys
from gensim import corpora, models, similarities
import logging, gensim
import pickle

print "loading dictionary"
dictionary = corpora.Dictionary().load('../model/comments_'+sys.argv[1]+'.dict') 
print dictionary

print "loading corpus"
mm = corpora.MmCorpus('../model/comments'+sys.argv[1]+'.mm')
print mm

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

print "training LDA model"
lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=int(sys.argv[2]), update_every=1, chunksize=10000, passes=5)
lda.print_topics()

save_name = '../model/lda_model_' + sys.argv[1] + '_' + '.pkl'
print 'saving model ', save_name
pickle.dump(lda, open(save_name, 'wd'))