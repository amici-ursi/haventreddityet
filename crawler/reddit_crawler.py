import praw
import pickle
import pprint 

reddit = praw.Reddit("Reddit_crawler")

#visited_subreddits_dic = dict()
#p = open("visited_dic.pkl","wd")
p_open = open("visited_dic.pkl","r")
visited_subreddits_dic = pickle.load(p_open)
p_open.close

delim = "|:|"
visit_limit = 10

#Start with random subreddit
current_subreddit = reddit.get_random_subreddit()

f1 = open("../data/comments.data","a")
#f1.write("subreddit|:|comment\n")
f2 = open("../data/subs.data","a")
#f2.write("subreddit|:|submission_title|:|url\n")
f3 = open("../data/com_redditors.csv","a")
#f3.write("subreddit,redditor\n")
f4 = open("../data/ratings.csv","a")
#f4.write("subreddit,redditor,rating\n")

def visit_limit_reached(subreddit_name):
	check = False
	if subreddit_name in visited_subreddits_dic:
		if visited_subreddits_dic[subreddit_name] >= visit_limit:
			print "/"*60
			print "VISIT LIMIT REACHED: ", subreddit_name
			print "/"*60
			check = True
	return check 

for k in range(1000):
    
    subreddit_set = set()
    comment_body_list = []
    comment_redditor_list = []
    
    try:
	if visit_limit_reached(current_subreddit.display_name):
        	current_subreddit = reddit.get_random_subreddit()
                continue
    
        current_subreddit_name = current_subreddit.display_name
        print "*"*60
        print "subreddit: ",current_subreddit_name
        print "*"*60
    
        #check to see if key is in dict
        if current_subreddit_name in visited_subreddits_dic:
            visited_subreddits_dic[current_subreddit_name] += 1
            print "/"*60
            print "ADDING ", visited_subreddits_dic[current_subreddit_name],"th to ", current_subreddit_name
            print "/"*60
        else:
            visited_subreddits_dic[current_subreddit_name] = 1
    
        #start form the top submisson
        try:
            subs = current_subreddit.get_top_from_month(limit = visit_limit)
        except:
            print "/"*60
            print "EXCEPTION: weird top of the month execption"
            print "/"*60
            current_subreddit = reddit.get_random_subreddit()
            continue 
    
        #avoid returning to the same submission
        i = 0
        while i < visited_subreddits_dic[current_subreddit_name]:
            try:
                current_submission = subs.next()
            except StopIteration:
                print "/"*60
                print "EXCEPTION: no next in submissions"
                print "/"*60
                break
            i += 1
    
        try:
            current_submission_title = current_submission.title
            print "submission: ", current_submission_title
            string_long = current_subreddit_name + delim + current_submission_title + delim + current_submission.url + "\n"
            f2.write(string_long.encode("utf8"))
        
        except:
            print "/"*60
            print "EXCEPTION: no title for submission? " 
            print "/"*60
            current_subreddit = reddit.get_random_subreddit()
            continue 
        print "+"*60
        
        c = 0
	
        for comment in current_submission.comments:
            if c >= 10: break
            c += 1
            try:    
                comment_body_list.append(comment.body)
                print "comment: ", comment.body
                string_long = current_subreddit_name + delim + comment.body + "\n"
                f1.write(string_long.encode("utf8"))
                
            except:
                print "/"*60
                print "EXCEPTION: no comment or body? " 
                print "/"*60
                continue 
            print "-"*60
    
            try:
                comment_redditor_list.append(comment.author.name)
                print "redditor: ", comment.author.name
                string_long = current_subreddit_name + "," + comment.author.name + "\n"
                f3.write(string_long.encode("utf8"))

            except:
                print "/"*60
                print "EXCEPTION: comment deleted? " 
                print "/"*60
                continue
            print "-"*60
    
        try:
            current_redditor = current_submission.comments[0].author
            current_redditor_name = current_redditor.name
            coms = current_redditor.get_comments()
            new_subreddit = coms.next().subreddit
            new_subreddit_name = new_subreddit.display_name
        except:
            print "/"*60
            print "EXCEPTION: redditor has no comments or display name?" 
            print "/"*60
            current_subreddit = reddit.get_random_subreddit()
            continue
        
	rating_dict = dict()
	sum_of_ratings = 0
        while 1:
            try: 
                new_subreddit = coms.next().subreddit
                new_subreddit_name = new_subreddit.display_name
                subreddit_set.add(new_subreddit_name)
		if new_subreddit_name in rating_dict:
		     rating_dict[new_subreddit_name] += 1
		else:
		     rating_dict[new_subreddit_name] = 1
		sum_of_ratings += 1
            except StopIteration:
                break
        
        print "*"*60
        for s in subreddit_set:
	    print s,",",current_redditor_name, " : " , float(rating_dict[s])/float(sum_of_ratings)
            string_long = s + "," + current_redditor_name + "\n"
            f3.write(string_long.encode("utf8"))
	    string_long = s + "," + current_redditor_name + "," + str(float(rating_dict[s])/float(sum_of_ratings)) + "\n"
	    f4.write(string_long.encode("utf8"))
        print "*"*60
        
        if len(subreddit_set)>=2:
            for subreddit_name in subreddit_set:
		if subreddit_name != current_subreddit_name and not visit_limit_reached(subreddit_name):
                   new_subreddit = reddit.get_subreddit(subreddit_name)
                   print "#"*60
                   print "GETTING SUBREDDIT ", subreddit_name
                   print "#"*60
                   break
        else:
            print "#"*60
            print "GETTING RANDOM SUBREDDIT"
            print "#"*60
            new_subreddit = reddit.get_random_subreddit()
        
        current_subreddit = new_subreddit
        
        if k%10==0:
            print "="*60
            print "SAVING DIC..."
            print "="*60
            
            p_save = open("visited_dic.pkl","w")
            pickle.dump(visited_subreddits_dic,p_save)
            p_save.close()
        
    except KeyboardInterrupt:
        print "Okay, Saving progress before exiting..."
        break
    
f1.close()
f2.close()
f3.close()
p_save = open("visited_dic.pkl","w")
pickle.dump(visited_subreddits_dic,p_save)
p_save.close()
