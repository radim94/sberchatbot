import stashy
from bitbucket_Api.common_bb import project_list, PR_list, repo_list
from stashy.pullrequests import PullRequest

BITBUCKET_SERVER = "http://172.30.18.187:7990"


def answer_project_list(args, answer, credentials):
    pl = project_list(credentials)
    # answer.selects = ({str(index + 1): proj['key'] for index, proj in enumerate(pl)}, 'Projects')
    answer.text = '\n'.join(proj['key'] for proj in pl)
    return answer


def answer_get_pr(args, answer, credentials):
    prs = [pr for pr in PR_list(credentials) if pr['state'] == 'OPEN']
    # answer.selects = ({str(index + 1): proj['title'] for index, proj in enumerate(prs)}, 'PRs')
    answer.text = '\n'.join(proj['title'] for proj in prs)
    return answer


def answer_repo_list(args, answer, credentials):
    pl = repo_list(args[0], credentials)
    answer.text = '\n'.join(proj['slug'] for proj in pl)
    return answer

def answer_approve(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    pr.approve()


def answer_decline(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    pr.decline()

def answer_merge(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    pr.merge()

def answer_unapprove(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    pr.unapprove()

def answer_get_comment(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    answer.text='\n'.join(
        x['comment']['author']['name'] + ':' + x['comment']['text'] for x in pr.activities() if
        x['action'] == 'COMMENTED')

def answer_jira_task(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    answer.text='\n'.join(x['key'] + '  :  ' + x['url'] for x in pr.issues())

def answer_get_commit(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
    answer.text='\n'.join(x['author']['name'] + '  :  ' + x['displayId'] for x in pr.commits())


