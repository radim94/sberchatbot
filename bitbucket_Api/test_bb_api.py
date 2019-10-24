# import cookielib
token = 'ODcyODIzMTY4NDE0Os0nGKYJTZm4ZM5/BnEg6ikmnFoO'
import requests
class API:
    def __init__(self,base_URL='localhost:7990'):
        self.sess=requests.Session()
        self.sess.verify=False
        self.sess.auth=requests.auth.HTTPBasicAuth("admin",token)
        self.base_url = base_URL
    def get(self,path):
        return self.get_raw(path)['values']
    def get_project(self,project):
        return self.get_raw('projects/{}'.format(project))
    def get_all_projects(self):
        return self.get('projects')
    def get_project_repos(self,project):
        return self.get('projects/{}/repos'.format(project))
    def get_repos_commits(self,project,repos):
        return self.get('projects/{}/repos/{}/commits'.format(project,repos))
    def get_repos_PR(self,project,repos):
        return self.get('projects/{}/repos/{}/pull-requests'.format(project,repos))
    def get_raw(self,path):
        print(path)
        ans=self.sess.get('http://{}/rest/api/1.0/{}?limit=10000'.format(self.base_url, path)).json()
        return ans
api=API()
print(api.get_all_projects())