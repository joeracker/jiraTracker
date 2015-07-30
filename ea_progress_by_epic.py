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

def display_active_epics_summary(epics_issues):
	print("POINTS PER EPIC:")
	for epic in epics_issues["epics"]:
		if epic["total_points_remain"] != 0:
			print("%s %s") % (epic["summary"], epic["total_points_remain"])

def display_active_epics_with_issues(epics_issues):
	print("DETAILED EPIC BREAKDOWN:")
	for epic in epics_issues["epics"]:
		if epic["total_points_remain"] != 0:
			print("%s %s") % (epic["summary"], epic["total_points_remain"])
			for issue in epic["stories"]:
				print("    %s %s %s") % (issue["key"], issue["summary"], issue["points"])

def OLDgroup_issues_by_epics(open_issues, epics):
	epic_statuses = {"epics":[]}
	i = 0
	for epic in epics:
		epic_statuses["epics"].append({
			"key": epic.key,
			"summary": epic.fields.summary,
			"total_points_remain": 0,
			"stories": []})
		issue_point_tally = 0
		for issue in open_issues:
			if epic_statuses["epics"][i]["key"] == issue.fields.customfield_10001:
				if issue.fields.customfield_10008 is None:
					points = 0
				else:
					points = int(issue.fields.customfield_10008)
				epic_statuses["epics"][i]["stories"].append({
					"key": issue.key,
					"summary": issue.fields.summary,
					"points": points})
				issue_point_tally = issue_point_tally + points

		epic_statuses["epics"][i]["total_points_remain"] = issue_point_tally
		i += 1
	
	return epic_statuses 

def group_issues_by_epics(open_issues, epics):
	epic_statuses = {"epics":[]}
	i = 0
	for epic in epics:
		epic_dict = {
			"key": epic.key,
			"summary": epic.fields.summary,
			"total_points_remain": 0,
			"stories": []}
		item = build_epic_dictionary_item(epic_dict, open_issues)
		epic_statuses["epics"].append(item)
		i += 1
	
	no_epic_item = get_issues_no_epic(open_issues)
	epic_statuses["epics"].append(no_epic_item)
	return epic_statuses

def get_issues_no_epic(open_issues):
	no_epic_item_dict = {
		"key": None,
		"summary": "No Epic Defined",
		"total_points_remain": 0,
		"stories": []}
	pprint(no_epic_item_dict)
	return build_epic_dictionary_item(no_epic_item_dict, open_issues)

def build_epic_dictionary_item(epic_item_dict, issues):
	issue_point_tally = 0
	for issue in issues:
		if epic_item_dict["key"] == issue.fields.customfield_10001:
			if issue.fields.customfield_10008 is None:
				points = 0
			else:
				points = int(issue.fields.customfield_10008)
			epic_item_dict["stories"].append({
				"key": issue.key,
				"summary": issue.fields.summary,
				"points": points})
			issue_point_tally = issue_point_tally + points
	epic_item_dict["total_points_remain"] = issue_point_tally
	return epic_item_dict

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

issues_and_epics = group_issues_by_epics(get_ea_open_issues(), get_epics())
print ""
display_active_epics_summary(issues_and_epics)
print ""
display_active_epics_with_issues(issues_and_epics)