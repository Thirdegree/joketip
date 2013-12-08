import praw
from time import sleep
from collections import deque
import re

r = praw.Reddit("Cocainetip bot by /u/Thirdegree")

def login_():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)

done = deque(maxlen=300)

Trying = True
while Trying:
	try:
		login_()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."


def is_tip(post_body):
	if "+/u/cocainetip"in post_body:
		after_split = post_body.split("+/u/cocainetip")[-1]
		cocaine = re.findall("[0-9]+ Oz. Cocaine", after_split)[0]
		if cocaine:
			oz = re.findall("[0-9]+", cocaine)[0]
			return oz
		return False
	return False

if __name__ == '__main__':
	while True:
		comments = r.get_comments("thirdegree")
		for post in comments:
			if post.id not in done:	
				oz = is_tip(post.body)
				done.append(post.id)
				if oz:
					parent_permalink = re.sub("[A-Za-z0-9]+$", re.sub("t[0-9]+_","", post.parent_id), post.permalink) 
					parent = r.get_submission(parent_permalink)
					sleep(2)
					parent_name = parent.comments[0].author.name
					print "**[Verified]**: /u/%s -> /u/%s **Cocaine (%s Oz.)**"%(parent_name, post.author.name, oz)
					post.reply("**[Verified]**: /u/%s -> /u/%s **Cocaine (%s Oz.)**"%(parent_name, post.author.name, oz))
					sleep(2)
		sleep(10)