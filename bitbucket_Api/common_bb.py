from dataclasses import dataclass
from enum import Enum

import stashy

class Steps(Enum):
    REPO_LIST='REPO_LIST'
    MANAGE_PR_OPTIONS = 'MANAGE_PR_OPTIONS'
    MANAGE_PR = 'MANAGE_PR'
    PR_LIST = 'PR_LIST'
    INIT = "init"
    START = 'start'
    PROJECT_LIST = 'project_list'

token = 'ODcyODIzMTY4NDE0Os0nGKYJTZm4ZM5/BnEg6ikmnFoO'
user='admin'
# token = '1'
# user='1'
stash = stashy.connect("http://172.30.18.187:7990", user,token)
stash
print(stash.projects.list())
def project_list():
    return stash.projects.list()
def repo_list(proj):
    return stash.projects[proj].list()
def PR_list():
    return stash.dashboard.pull_request.list()

@dataclass
class State:
    project:str=None
    repository:str=None
    pull_request:str=None
    step:str= Steps.INIT

if __name__ == '__main__':

    state = State()
    print(stash.dashboard)
    print(stash.dashboard.pull_request.get())
    print(stash.dashboard.pull_request.list()[0])
    pr=PR_list()[0]
    state.repository = pr['fromRef']['repository']['slug']
    state.project = pr['fromRef']['repository']['project']['key']
    state.pull_request = pr['id']
    # q=pull_requests[state.pull_request]
    print(q.diff())
    # q.merge(version=pr['version'])