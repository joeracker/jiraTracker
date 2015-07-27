from search import Search
from pprint import pprint
import json

search_query = """
		project = 'Cloud DNS' 
		AND priority = Blocker
		AND status not in (Closed, "Ready for Release")
	"""
labels = [
	'Access',
	'Performance',
	'Monitoring',
	'Support',
	]

def get_issues_with_label():
	i = 0
	y = 0
	for label in labels:
		issues = Search(search_query + "AND labels = '%s'" % label)
		print(label)
		print("%s total issues. %s total points.") % (
			issues.get_issue_count(), issues.get_point_sum())
		i = i + issues.get_point_sum()
		y = y + issues.get_issue_count()
	print("Total issues: %s Total Points: %s") % (y, i)

def get_issues_no_label():
	issues = Search(search_query + "AND labels NOT IN('%s')" % label)
	print(label)
	print("%s total issues. %s total points.") % (
		issues.get_issue_count(), issues.get_point_sum())

def get_issues_open_ea_by_epic():
	# get list of issues
	issues = Search(search_query)
	return issues

	# group the issues by epic
	# provide metrics by epic

#get_issues_with_label()
#pprint(dir(get_issues_open_ea_by_epic()))
print(json.dumps(get_issues_open_ea_by_epic, 
                 default=lambda obj: vars(obj),
                 indent=1))
