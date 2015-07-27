import sys
sys.path.append('/Users/jmcbride/Code/jira-python')

from jira.client import JIRA
import datetime

options = {
    'server': 'https://jira.rax.io'
}


search_query = """
		project = 'Cloud DNS' 
		AND priority = Blocker
		AND status not in (Closed, "Ready for Release")
	"""

jira = JIRA(options=options)
search_response = jira.search_issues(search_query, maxResults=30000)

def print_all_issues_important_values():
	for issue in search_response:
		print("%s - %s - %s - %s") % (
			issue.key,
			issue.fields.summary,
			issue.fields.customfield_10001,
			issue.fields.customfield_10008,
		)

def get_all_epics():
	# use a search to get them into a list

def get_issues_by_epics(epics):
	# get the list of issues we care about from search
	for n in search_response:
	    if n.fields.customfield_10001 == "DNS-152":
			print n.key


# get_all_epics
# find issues with epic and blocker and open and cloud DNS