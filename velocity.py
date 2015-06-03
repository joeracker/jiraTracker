# Gets velocity and related stuff

#import imp
import sys

sys.path.append('/Users/jmcbride/Code/jira-python')
#print sys.path

from jira.client import GreenHopper
from jira.exceptions import *

options = {
    'server': 'https://jira.rax.io'
}
gh = GreenHopper(options)
e = JIRAError()

# Get all boards available
boards = gh.boards

# Get the DNS board
board_id = 41
#print("Story board: %s (%s)" % (boards[0].name, board_id))
#print("Story board: %s" % (boards[0].name))
#print("Story board: %s" % (board_id), boards)

sprints = gh.sprints(board_id)


# List all sprints
print("%s Sprints for this board:") % (len(sprints))
print("=========================")
for sprint in sprints:
	if e:
		sprint_id = sprint.id
		print("%s, %s" % (sprint.name, sprint.id))
		#print(gh.sprint_info(board_id, sprint.id))
		#incomplete_issues = gh.incomplete_issues(board_id, sprint_id)
		#print gh.completedIssuesEstimateSum(board_id, sprint_id)
		try:
			print gh.completedIssuesEstimateSum(board_id, sprint_id)
		except:
			e = sys.exc_info()[0]
			print( "Error: %s" % e )
	#	print jira.exceptions


#sprint_report = "https://jira.rax.io/rest/greenhopper/1.0/rapid/charts/sprintreport?rapidViewId=41&sprintId=179"