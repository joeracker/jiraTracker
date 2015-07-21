from search import Search
import sys

###### Sprint Closing Metrics ########
if len(sys.argv) > 1:
	current_sprint = sys.argv[1]
else:
	print("Sprint ID required. Example: script_name.py 3234")
	sys.exit()

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

#ea_
