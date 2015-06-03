# TODO: refactor to use search.py module and class
# TODO: Need to rename this module, as this script gives a summary on how we are
#       tracking to EA launch

import sys
sys.path.append('/Users/jmcbride/Code/jira-python')

from jira.client import JIRA
import datetime

options = {
    'server': 'https://jira.rax.io'
}
jira = JIRA(options)



# print the object returned from a search
search_response_summary = "Designate Early Access Items"

# COMMONLY USED QUERIES: (use the "search" class for this instead)
# All open items in EA
#search_query = 'priority = Blocker AND project = "Cloud DNS" AND status not in ("Research Done", "closed") ORDER BY cf[10008] DESC'
# Closed EA items in a specific sprint
search_query = 'priority = Blocker AND project = "Cloud DNS" AND Sprint = 778 AND status in ("Research Done", "closed") ORDER BY cf[10008] DESC'
# Query for stuff completed by assignee
#search_query = 'assignee = timo6371 AND status in ("Research Done", "closed") and updated > 2014-07-01'



#search_query = 'priority = Blocker AND project = "Cloud DNS" AND Sprint = 594 AND status in ("Research Done", "closed") ORDER BY cf[10008] DESC'
search_response = jira.search_issues(search_query, maxResults=30000)
#print search_response

# print open issues with key, points, summary

#for issue in search_response:
#    print "%s - %s - %s" %(issue.key, issue.fields.customfield_10008, issue.fields.summary)



# print total open stories
print ""
#print search_response_summary
print "JIRA Search Query: %s" % search_query
print "Open Stories: %s" %(len(search_response))

# print total backlog points
backlog_points_sum = 0
no_estimate = 0
for issue in search_response:
	try:
	    story_points = int(issue.fields.customfield_10008)
	except TypeError:
		story_points = 0
		no_estimate = no_estimate + 1
	backlog_points_sum = backlog_points_sum + story_points

print "Unestimated Stories: %s" %(no_estimate)
print "Total Points in Backlog: %s" %(backlog_points_sum)

# Sprints required at x velocity
weeks_in_sprint = 3
velocity_last_10_sprints = [66, 34, 59, 26, 39, 75, 109, 81, 91, 71]
velocity = sum(velocity_last_10_sprints)/len(velocity_last_10_sprints) - 8
velocity = 76 - 10
sprints_remaining = backlog_points_sum/velocity
weeks_remain = sprints_remaining*weeks_in_sprint
months_remain = round(weeks_remain/4.3, 1)
estimated_completion_date = (datetime.date.today() + datetime.timedelta(weeks_remain*7)).isoformat()

print ""
print "TIME REMAINING:"
print "Velocity: %s" % (velocity)
print "Sprints: %s" % (sprints_remaining)
print "Weeks: %s" % (weeks_remain)
print "Months: ~%s" % (months_remain)
print "ETA: %s" % (estimated_completion_date)

# new stories since x