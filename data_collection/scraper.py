
# coding: utf-8

## Reddit Scraper

# This scraper is designed for finding descriptions of subreddits from the reddit.com/subreddits pages. I made this scraper because this information does not seem to be available via their API.  

#### Scraping functions

import time, pickle, requests
import numpy as np

#functions for finding respective fields 

def get_substring(text, pos, start_str, end_str):
    i_start = text.find(start_str,pos)
    pos = i_start 
    if i_start < 0: 
        return pos, 'None'
    pos += len(start_str)
    i_end = text.find(end_str,pos)
    return pos, text[pos:i_end]

def get_description(text, pos):
    start_str = '<div class="usertext-body may-blank-within md-container"><div class="md">'
    end_str = '</div>'
    return get_substring(text, pos, start_str, end_str)


def get_title(text, pos):
    start_str = 'class="title" >/r/'
    end_str = '</a>'
    return get_substring(text, pos, start_str, end_str)

def get_nsubscribers(text,pos):
    start_str = 'subscribers</span></span><span class="score likes"><span class="number">'
    end_str = '</span>'
    return get_substring(text, pos, start_str, end_str)

def get_age(text,pos):
    start_str = '</span>, a community for '
    end_str = '</p>'
    return get_substring(text, pos, start_str, end_str)

def get_next_url(text,pos, it):
    if it ==0:
        start_str = '<span class="nextprev">view more:&#32;<a href="'        
    else:
        start_str = '</a><span class="separator"></span><a href="'
    end_str = '" rel="nofollow next" >'
    return get_substring(text,pos,start_str,end_str)


#### Starting conditions 

#start from fresh
#subr_des = dict()
#url = 'http://reddit.com/subreddits'

#or start from where the previous session stopped
subr_des = pickle.load(open('description3_dict.pkl','rd'))
url = subr_des['current_url']

#sub_dict = pickle.load(open('../data/sub_dict.pkl','rd'))

#### Data collection

for sub in sub_dict:
    
    #reddit doesn't like scrapers
    while True:
        try:
            text = requests.get(url).text
    	    n_url = get_next_url(text,0,len(subr_des))[1]
            #n_url = 'http://www.reddit.com/subreddits/search?q='+sub
            if text.find('<title>Too Many Requests</title>')<0 and n_url != 'None':
                break
	    	randn = np.random.exponential(2)
            print 'sleeping for ', randn
            time.sleep(randn)
        except:
            print 'connection error'
            randn = np.random.exponential(2)
            print 'sleeping for ', randn
            time.sleep(randn)
        
    pos = [0]*4
    while pos[3] >= 0:
        pos[0], title = get_title(text, pos[0])
        pos[1], description = get_description(text, pos[1])
        pos[2], nsubscribers = get_nsubscribers(text, pos[2])
        pos[3], age = get_age(text, pos[3])
        
        #check to see if the last title has been found
        if  pos[0] < 0:
            break
            
        #If there is no description it will read the next one
        if pos[1]>pos[2]:
            description =' '
            pos[1] = pos[0]
            
        #save as a hash map for quick access
        key = title[:title.find(':')].lower()
        subr_des[key] = [title,description,nsubscribers,age]
    	subr_des['current_url'] = url
    
    #dump once a page
    #make a backup incase program exits while dumping
    if i % 2 == 0:
    	pickle.dump(subr_des, open('description3_dict.pkl','wd'))
    else:
		pickle.dump(subr_des, open('description2_dict.pkl','wd'))    

    #hacky way to deal with &amp accumulations 
    amp_start = n_url.find('amp=&amp')
    if amp_start > 0:
        amp_end = n_url.find('&amp;count')
        url = n_url[:amp_start]+n_url[amp_end+5:]
    else:
        url = n_url
    
    print "page ", i+1
    print "subs ", len(subr_des)
    print "next url", url 
    
    #reddit doesn't like scrapers
    randn = np.random.exponential(2)
    print 'sleeping for ', randn
    time.sleep(randn)

