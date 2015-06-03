import sys
sys.path.append('/Users/jmcbride/Code/jira-python')

from jira.client import JIRA
import datetime

options = {
    'server': 'https://jira.rax.io'
}

class Search():

	def __init__(self, query):
		jira = JIRA(options=options)
		self.search_response = jira.search_issues(query, maxResults=30000)
		#print "Query: '%s'" % query
		#print self.search_response

	def get_point_sum(self):
		backlog_points_sum = 0
		#print self.search_response
		no_estimate = 0
		for issue in self.search_response:
			try:
			    story_points = int(issue.fields.customfield_10008)
			    
			except TypeError:
				story_points = 0
				no_estimate = no_estimate + 1
			backlog_points_sum = backlog_points_sum + story_points

		return backlog_points_sum

	def get_issue_count(self):
		return len(self.search_response)
		pass

	def get_issue_count_no_estimate():
		# TODO make this work
		no_estimate = 0
		for issue in search_response:
			try:
			    story_points = int(issue.fields.customfield_10008)
			except TypeError:
				story_points = 0
				no_estimate = no_estimate + 1
			backlog_points_sum = backlog_points_sum + story_points		#return "Issues with no estimate: %s" %(no_estimate)
		pass

##### This should be refactored into it's own class

###### Sprint Closing Metrics ########
current_sprint = 1128

# https://one.rackspace.com/display/cdns/Sprint+Planning
issues_closed = Search(
	'project = "Cloud DNS"'
	' AND Sprint in (%s)'
	' AND status in ("Research Done", "closed")'
	' ORDER BY cf[10008] DESC' % current_sprint)
print("%s total issues. %s total points.") % (
	issues_closed.get_issue_count(), issues_closed.get_point_sum())

ea_issues_closed = Search(
	'priority = Blocker'
	' AND project = "Cloud DNS"'
	' AND Sprint = %s'
	' AND status in ("Research Done", "closed")'
	'  ORDER BY cf[10008] DESC' % current_sprint)
print("%s EA issues. %s EA points.") % (ea_issues_closed.get_issue_count(), ea_issues_closed.get_point_sum())

ea_remain = Search('priority = Blocker'
	' AND project = "Cloud DNS"' 
	' AND status not in ("closed")')
print("%s issues and %s pointsremain in EA") % (ea_remain.get_issue_count(), 
	ea_remain.get_point_sum())

# print ("================================")

# print ("Points completed %s" % issues_closed.get_point_sum())
# print ("Points remain %s" % ea_issues_closed.get_point_sum())

# print ("Issues Completed: %s" % issues_closed.get_issue_count())
# print ("Issues Remain %s " % ea_issues_closed.get_issue_count())

#Get list of all sprints for project, calculate the velocity


