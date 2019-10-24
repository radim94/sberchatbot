from bitbucket_Api.common_bb import project_list, PR_list, repo_list


def answer_project_list(args, answer, credentials):
    pl = project_list(credentials)
    answer.selects = ({str(index + 1): proj['key'] for index, proj in enumerate(pl)}, 'Projects')
    return answer


def answer_get_pr(args, answer, credentials):
    prs = [pr for pr in PR_list(credentials) if pr['state'] == 'OPEN']
    answer.selects = ({str(index + 1): proj['title'] for index, proj in enumerate(prs)}, 'PRs')
    return answer


def answer_get_pr(args, answer, credentials):
    pl = repo_list(args[0], credentials)
    answer.selects = ({str(index + 1): proj['slug'] for index, proj in enumerate(pl)}, 'Repos')
    return answer
