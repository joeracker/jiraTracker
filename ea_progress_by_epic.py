from search import Search
import sys
from pprint import pprint
sys.path.append('/Users/jmcbride/Code/jira-python')

from jira.client import JIRA
import datetime
import json


options = {
    'server': 'https://jira.rax.io'
}

def group_issues_by_epics(open_issues, epics):
	# get the list of issues we care about from search
	epic_statuses = load_sample_json()
	i = 0
	for epic in epics:
		#print epic_statuses[1]["key"]
		epic_statuses["epics"][i]["key"] = epic.key
		epic_statuses["epics"][i]["summary"] = epic.fields.summary
		print("EPIC: %s %s") % (epic.key, epic.fields.summary)
		print("==========================")
		y = 0
		for issue in open_issues:
			if issue.fields.customfield_10001 == epic.key:
				print("    %s - %s - %s") % (
					issue.key,
					issue.fields.summary,
					issue.fields.customfield_10008,
				)
				if len(epic_statuses["epics"][i]["stories"]) > y:
						# http://stackoverflow.com/questions/8789279/how-to-make-a-nested-dictionary-and-dynamically-append-data
				epic_statuses["epics"][i]["stories"][y]["key"] = issue.key
				epic_statuses["epics"][i]["stories"][y]["summary"] = issue.fields.summary
				if isinstance(issue.fields.customfield_10008,(int,long)):
					epic_statuses["epics"][i]["total_points_remain"] += int(issue.fields.customfield_10008)
					epic_statuses["epics"][i]["stories"][y]["points"] = issue.fields.customfield_10008
				else:
					epic_statuses["epics"][i]["total_points_remain"] += 0
					epic_statuses["epics"][i]["stories"][y]["points"] = 0

				y += 1
				print y
		print ("")
		i += 1
		print i

def get_ea_open_issues():
	search_query = """
		project = 'Cloud DNS' 
		AND priority = Blocker
		AND status not in (Closed, "Ready for Release")
	"""
	jira = JIRA(options=options)
	return jira.search_issues(search_query, maxResults=30000)

def get_epics():
	epic_query = """
		project = DNS AND Type = Epic
	"""
	jira = JIRA(options=options)
	return jira.search_issues(epic_query, maxResults=30000)

def load_sample_json():
	with open('sample_epics_with_Issues.json') as data_file:
		loaded_json = json.load(data_file)
		#pprint(loaded_json)
		return loaded_json


# get_all_epics
#for item in get_epics(): print item.key, item.fields.summary
# find issues with epic and blocker and open and cloud DNS

group_issues_by_epics(get_ea_open_issues(), get_epics())