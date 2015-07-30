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
	epic_statuses = {"epics":[]}
	i = 0
	for epic in epics:
		print("start epic")
		epic_statuses["epics"].append({
            "key": epic.key,
            "summary": epic.fields.summary,
            "total_points_remain": 0,
            "stories": []})

        print("mid")
        y = 0
        for issue in open_issues:
        	#print "  start child issue filter"
        	#print("  %s = %s") % (epic_statuses["epics"][i]["key"], issue.fields.customfield_10001)
        	if epic_statuses["epics"][i]["key"] == issue.fields.customfield_10001:
        		#print "  ***** match"
        		epic_statuses["epics"][i]["stories"].append({
            	    "key": issue.key,
            	    "summary": issue.fields.summary,
            	    "points": issue.fields.customfield_10008
        		})
        	y += 1
        	#print("  y = %s") % y

    	i += 1
    	print("epic i = %s") % (i)
	pprint(epic_statuses)


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