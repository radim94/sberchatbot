from pprint import pprint
import re


class JIRA_API:

    def __init__(self, server, login, password):
        try:
            import jira
        except ImportError:
            raise IndexError('Install jira (pip install jira')
        self.obj: jira.JIRA = jira.JIRA(server=server, basic_auth=(login, password))
        self.current_project = None
        self.current_issue = None

    def get_assigned_issue(self):
        user = self.obj.current_user()
        issues = self.obj.search_issues(f'assignee={user} AND statuscategory != Done')
        return {issue.key: f'{issue.fields.project} / {issue.key}' for issue in issues}

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
        return self.obj.assign_issue(issue, whom)

    def t(self):
        user = self.obj.current_user()
        # print(user)
        # res = self.obj.search_issues('sprint in openSprints()')
        # print(res)
        res = self.obj.search_issues(f'assignee={user}')
        pprint(dir(res[0].fields))
        # pprint(res[0].fields.customfield_10105)
        # print('sprint' in res[0].fields.customfield_10100)
        # for sprint in res[0].fields.customfield_10000:
            # sprint_name = re.findall(r"name=[^,]*", str(res[0].fields.customfield_10000[0]))
            # print(sprint_name)
            # print(sprint)
            # pass

        # pprint([(dir(x.fields), x.id, x.key, x.fields.customfield_10104) for x in res])
        # pprint(self.obj.fields())


if __name__ == '__main__':
    jira_obj = JIRA_API(server='http://172.30.18.111:8080', login='1', password='1')
    # pprint(jira_obj.get_projects())
    # jira_obj.select_project(10000)
    # pprint(jira_obj.get_issue_types())
    jira_obj.t()
    # pprint(jira_obj.create_issue('New task', 'Bug'))
    # pprint(jira_obj.create_issue('New task', 'Bug').permalink())
    # print(projects)
    # pprint(meta['projects'])
