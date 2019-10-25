# import cookielib
from pprint import pprint

token = 'ODcyODIzMTY4NDE0Os0nGKYJTZm4ZM5/BnEg6ikmnFoO'
user='admin'
import requests
class API:
    def __init__(self,base_URL='172.30.18.215:7990'):
        self.sess=requests.Session()
        self.sess.verify=False
        self.sess.auth=requests.auth.HTTPBasicAuth("admin",token)
        self.base_url = base_URL
    def get(self,path):
        return self.get_raw(path)['values']
    def get_project(self,projectKey):
        return self.get_raw(f'projects/{projectKey}')
    def get_all_projects(self):
        return self.get('projects')
    def get_project_repos(self,projectKey):
        return self.get(f'projects/{projectKey}/repos')
    def get_repos_commits(self,projectKey,repositorySlug):
        return self.get(f'projects/{projectKey}/repos/{repositorySlug}/commits')
    def get_repos_PR(self,projectKey,repositorySlug):
        return self.get(f'projects/{projectKey}/repos/{repositorySlug}/pull-requests')
    def approve_PR(self,projectKey,repositorySlug,pullRequestId):
        return self.post(f'projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/approve')
    def approve_PR(self,projectKey,repositorySlug,pullRequestId):
        return self.post(f'projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/approve')
    def merge_PR(self,projectKey,repositorySlug,pullRequestId):
        return self.post(f'projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/merge')

    def get_current_user_PRs(self,state='',role='',participantStatus='',order='',closedSince=''):
        return self.get(f'dashboard/pull-requests')
    def get_project_repo_PR_tasks(self,project,repo,pr_id):
        ans = self.sess.get(f'http://{self.base_url}/rest/jira/1.0/projects/{project}/repos/{repo}/pull-requests/{pr_id}/issues?limit=10000')
        ans = ans.json()
        return ans
    def get_raw(self,path):
        print(path)
        ans=self.sess.get('http://{}/rest/api/1.0/{}?limit=10000'.format(self.base_url, path))
        ans=ans.json()
        return ans
    def post(self,path):
        print('http://{}/rest/api/1.0/{}'.format(self.base_url, path))
        ans= self.sess.post('http://{}/rest/api/1.0/{}'.format(self.base_url, path),headers={'X-Atlassian-Token': 'no-check'})
        return ans
api=API()
print(api.get_all_projects())
# pprint(api.get_current_user_PRs())
# pprint(api.get_repos_PR('TEST','repo_1'))
# input("+=====================================")
# pprint(api.approve_PR('TEST','repo_1',2))
# input("+=====================================")
# pprint(api.get_repos_PR('TEST','repo_1'))
pprint(api.get_project_repo_PR_tasks('TEST','repo_1',4))
