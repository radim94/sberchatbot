class JIRA_API:

    def __init__(self, server, login, password):
        try:
            import jira
        except ImportError:
            raise IndexError('Install jira (pip install jira')
        self.obj: jira.JIRA = jira.JIRA(server=server, basic_auth=(login, password))

    def get_assigned_issue(self):
        user = self.obj.current_user()
        issues = self.obj.search_issues(f'assignee={user} AND statuscategory != Done')
        return {f'tasks {issue.key}': f'{issue.fields.project} / {issue.key}' for issue in issues}

    def get_issue_info(self, issue_key):
        issue = self.obj.search_issues(f'key={issue_key}')[0]
        return {
            'key': issue.key,
            'summary': issue.fields.summary,
            'description': issue.fields.description,
            'status': issue.fields.status
        }

    def transition_issue(self, transition, issue_key):
        issue = self.obj.search_issues(f'key={issue_key}')[0]
        transitions = self.get_issue_transition(issue_key)
        self.obj.transition_issue(issue, transition)
        if transition.isnumeric():
            return transitions[transition]
        else:
            return transition.title()

    def get_issue_transition(self, issue_key):
        issue = self.obj.search_issues(f'key={issue_key}')[0]
        transition = self.obj.transitions(issue)
        return {x['id']: x['name'] for x in transition}

    def get_issues_in_sprint(self):
        issues = self.obj.search_issues('sprint in openSprints()')
        return {issue.key: f'{issue.fields.project} / {issue.key} ({issue.fields.status})' for issue in issues}

    def assign_issue(self, issue_key, whom=None):
        if not whom:
            whom = self.obj.current_user()
        issue = self.obj.search_issues(f'key={issue_key}')[0]
        self.obj.assign_issue(issue, whom)
        return whom

