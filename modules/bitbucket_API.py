import stashy
from bitbucket_Api.common_bb import project_list, PR_list, repo_list
from stashy.errors import NotFoundException
from stashy.pullrequests import PullRequest

BITBUCKET_SERVER = "http://172.30.18.187:7990"

def answer_bitbucket(args, answer, credentials):
    answer.text='''available commands:
    projects -- get list of projects;
    repo <PROJECT> -- get repos of selected project
    pr -- get list available pull-request
    approve <PROJECT> <REPO> <PR> -- approve selected PR
    unapprove <PROJECT> <REPO> <PR> -- unapprove selected PR 
    decline <PROJECT> <REPO> <PR> -- decline selected PR 
    merge <PROJECT> <REPO> <PR> -- merge selected PR 
    pr comments <PROJECT> <REPO> <PR> -- get comments for selected PR 
    pr tasks <PROJECT> <REPO> <PR> -- get linked jira task for selected PR 
    commits <PROJECT> <REPO> <PR> -- get commits of selected PR 
    new comment <PROJECT> <REPO> <PR> <COMMENT> -- add comment to selected PR 
    bitbucket -- this help
    '''

def answer_projects(args, answer, credentials):
    pl = project_list(credentials)
    # answer.selects = ({str(index + 1): proj['key'] for index, proj in enumerate(pl)}, 'Projects')
    answer.text = '\n'.join(proj['key'] for proj in pl)
    return answer

def answer_get(args,answer,credentials):
    if args[0]=='comment':
        answer_comments(args[1:],answer,credentials)
    elif args[0]=='commit':
        answer_commits(args[1:],answer,credentials)

def answer_pr(args, answer, credentials):
    if len(args)!=0:
        if args[0]=='comments':
            return answer_comments(args[1:], answer, credentials)
        elif args[0]=='tasks':
            return answer_jira_task(args[1:], answer, credentials)
        else:
            answer.text='''you can use "pr comments", "pr tasks" or "PR"'''
            return 
    prs = [pr for pr in PR_list(credentials) if pr['state'] == 'OPEN']
    # answer.selects = ({str(index + 1): proj['title'] for index, proj in enumerate(prs)}, 'PRs')
    answer.text = '\n'.join(proj['title'] for proj in prs)
    return answer

def answer_repo(args,answer,credentials):
    answer_repositories(args,answer,credentials)

def answer_repositories(args, answer, credentials):
    if len(args)!=1:
        answer.text='Use repo <PROJECT>'
        return
    try:
        pl = repo_list(args[0], credentials)
        answer.text = '\n'.join(proj['slug'] for proj in pl)
    except NotFoundException:
        answer.text = f'project {args[0]} not found'
    return answer

def answer_approve(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])

    if len(args)!=3:
        answer.text='Use approve <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        pr.approve()
        answer.text='PR approved'
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_decline(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 3:
        answer.text = 'Use decline <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        pr.decline()
        answer.text = 'PR declined'
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_merge(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 3:
        answer.text = 'Use merge <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        pr.merge()
        answer.text='PR merged'
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_unapprove(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])

    if len(args) != 3:
        answer.text = 'Use unapprove <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        pr.unapprove()
        answer.text='PR unapproved'
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_comments(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 3:
        answer.text = 'Use pr comments <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        answer.text = '\n'.join(
            x['comment']['author']['name'] + ':' + x['comment']['text'] for x in pr.activities() if
            x['action'] == 'COMMENTED')
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_jira_task(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 3:
        answer.text = 'Use pr tasks <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        answer.text='\n'.join(x['key'] + '  :  ' + x['url'] for x in pr.issues())
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_commits(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 3:
        answer.text = 'Use commits <PROJECT> <REPO> <PR>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        answer.text = '\n'.join(x['author']['name'] + '  :  ' + x['displayId'] for x in pr.commits())
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

def answer_new(args, answer, credentials):
    if len(args)>0 and args[0]=='comment':
        answer_new_comment(args[1:], answer, credentials)
    else:
        answer.text='Use new comment <PROJECT> <REPO> <PR> <COMMENT>'
def answer_new_comment(args, answer, credentials):
    pr: PullRequest
    stash = stashy.connect(BITBUCKET_SERVER, credentials['login'], credentials['password'])
    if len(args) != 4:
        answer.text = 'Use new comment <PROJECT> <REPO> <PR> <COMMENT>'
        return
    try:
        pr = stash.projects[args[0]].repos[args[1]].pull_requests[args[2]]
        pr.comment(' '.join(args[3:]))
    except NotFoundException:
        answer.text = f'project {args[0]} not found'

