from jira import JIRA
import feedparser
import legacy.bot_properties as bp
#FIXME repeated import

skype_bot_code,skype_bot_password,webhook,trello_user_KEY,trello_user_token,trello_user_board_id,jira_user,jira_password,jira_server,trello_list,jira_project=bp.read_properties()


def add_task_jira(summary: str):
    summary = summary.replace('\n', '')
#'https://sbtatlas.sigma.sbrf.ru/jira'
    jira_1 = JIRA(jira_server, basic_auth=(jira_user, jira_password), get_server_info=False,
                  options={'verify': False})
    new_issue = jira_1.create_issue(project=jira_project, summary=summary, issuetype={'name': 'Task'})



def jira_main(): # просто солянка выдержек из api на будущее
    jira = JIRA()

    jac = JIRA('https://jira.atlassian.com')

    auth_jira = JIRA(basic_auth=('username', 'password'))

    issue = jira.issue("JRA-1330")

    summary = issue.fields.summary  # 'Field level security permissions'
    votes = issue.fields.votes.votes  # 440 (at least)

    issue = jira.issue('JRA-1330', fields='summary,comment')

    # requires issue assign permission, which is different from issue editing permission!
    jira.assign_issue(issue, 'newassignee')

    new_issue = jira.create_issue(project='PROJ_key_or_id', summary='New issue from jira-python',
                                  description='Look into this one', issuetype={'name': 'Bug'})

    issue_dict = {
        'project': {'id': 123},
        'summary': 'New issue from jira-python',
        'description': 'Look into this one',
        'issuetype': {'name': 'Bug'},
    }
    new_issue = jira.create_issue(fields=issue_dict)

    issue_list = [
        {
            'project': {'id': 123},
            'summary': 'First issue of many',
            'description': 'Look into this one',
            'issuetype': {'name': 'Bug'},
        },
        {
            'project': {'key': 'FOO'},
            'summary': 'Second issue',
            'description': 'Another one',
            'issuetype': {'name': 'Bug'},
        },
        {
            'project': {'name': 'Bar'},
            'summary': 'Last issue',
            'description': 'Final issue of batch.',
            'issuetype': {'name': 'Bug'},
        }]

    issues = jira.create_issues(field_list=issue_list)
    jira_1 = JIRA('https://sbtatlas.sigma.sbrf.ru/jira', basic_auth=('14691412', "@L1a6a08!#"), get_server_info=False,
                  options={'verify': False})

    users = jira_1.search_users('Автаев Александр')
    # user=users[0]
    users
    # user.find(12345)

    import requests

    # jira._get_json('plugins/servlet/streams?maxResults=10&relativeLinks=true&streams=user+IS+sbt-galaktionov-aa2&_=1521703681298')
    url = jira_1._get_url(
        'plugins/servlet/streams?maxResults=100&relativeLinks=false&streams=user+IS+sbt-galaktionov-aa2',
        base='{server}/{path}')
    text = jira_1._session.get(url).text
    rss = feedparser.parse(text)
    # requests.get('https://sbtatlas.sigma.sbrf.ru/jira/plugins/servlet/streams?maxResults=10&relativeLinks=true&streams=user+IS+sbt-galaktionov-aa2&_=1521703681298')


