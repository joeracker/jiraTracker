from jira.client import JIRA

options = {
    'server': 'https://jira.rax.io'
}
jira = JIRA(options)

# print the object returned from a search
search_response = jira.search_issues('priority = Blocker AND project = "Cloud DNS" ORDER BY cf[10008] DESC', maxResults=30000)
#print search_response

# print open issues with key, points, summary

#for issue in search_response:
#    print "%s - %s - %s" %(issue.key, issue.fields.customfield_10008, issue.fields.summary)

# print total open stories
print ""
print "=================================="
print "GENERAL STATS:"
print "Open Stories: %s" %(len(search_response))

# print total backlog points
backlog_sum = 0
no_estimate = 0
for issue in search_response:
	try:
	    story_points = int(issue.fields.customfield_10008)
	except TypeError:
		story_points = 0
		no_estimate = no_estimate + 1
	backlog_sum = backlog_sum + story_points

print "Total Points in Backlog: %s" %(backlog_sum)

# unestimated stories
print "Unestimated Stories: %s" %(no_estimate)

# New Stuff
print ""
print "=================================="
print "NEW STUFF:"
print "TBD"

# Sprints required at x velocity
weeks_in_sprint = 3
velocity = 45
sprints_remaining = backlog_sum/velocity
print ""
print "=================================="
print "TIME REMAINING:"
print "Sprints remaining at %s velocity: %s" %(velocity,sprints_remaining)
print "%s weeks remain." %(sprints_remaining*weeks_in_sprint)

# new stories since x