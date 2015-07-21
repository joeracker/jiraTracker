from search import Search

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

get_issues_with_label()
