import sys
sys.path.append('/Users/jmcbride/Code/jira-python')

from jira.client import JIRA
import datetime

options = {
    'server': 'https://jira.rax.io'
}

class Search(object):

	def __init__(self, query):
		jira = JIRA(options=options)
		self.search_response = jira.search_issues(query, maxResults=30000)
		#print "Query: '%s'" % query
		#print self.search_response

	def get_issue_list(self):
		return self.search_response

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


