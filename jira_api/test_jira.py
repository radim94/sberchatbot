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
        self.obj.transition_issue(issue, transition)
        return self.get_issue_info(issue_key)

    def get_issue_transition(self, issue_key):
        issue = self.obj.search_issues(f'key={issue_key}')[0]
        transition = self.obj.transitions(issue)
        return {x['id']: x['name'] for x in transition}




    def get_projects(self):
        projects = self.obj.projects()
        return projects

    def select_project(self, project_id):
        self.current_project = project_id

    def get_issue_types(self):
        assert self.current_project is not None, 'Select project bt JIRA_API.select_project'
        meta = self.obj.createmeta(projectIds=[self.current_project])
        return [{'name': x['name']} for x in meta['projects'][0]['issuetypes']]

    def create_issue(self, summary, issuetype, description=None):
        issue = {
            'project': {'id': self.current_project},
            'summary': summary,
            'issuetype': {'name': issuetype},
        }
        if description is not None:
            issue['description'] = description

        return self.obj.create_issue(fields=issue)

    def select_issue(self, issue_id):
        self.current_issue = issue_id

    def unselect_project(self):
        self.current_project = None

    def unselect_issue(self):
        self.current_issue = None

    def t(self):
        user = self.obj.current_user()
        # print(user)
        res = self.obj.search_issues('sprint in openSprints()')
        print(res)
        # res = self.obj.search_issues(f'assignee={user}')
        # pprint(dir(res[0].fields))
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
    pprint(jira_obj.get_projects())
    jira_obj.select_project(10000)
    pprint(jira_obj.get_issue_types())
    jira_obj.t()
    # pprint(jira_obj.create_issue('New task', 'Bug'))
    # pprint(jira_obj.create_issue('New task', 'Bug').permalink())
    # print(projects)
    # pprint(meta['projects'])
