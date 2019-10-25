import jenkins
import random
import string
from jenkins_integrations.jenk2 import create_job
from jenkins_integrations import jenk2

JENKINS_SERVER = "http://172.30.18.110:8080"


def answer_hello_user(args, answer, credentials):
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    user = server.get_whoami()
    version = server.get_version()
    answer.text = 'Hello %s from Jenkins %s' % (user['fullName'], version)
    return answer


def answer_get_jobs_count(args, answer, credentials):
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    answer.text = 'На сервере сейчас %d джоб' % server.jobs_count()
    return answer


def answer_create_job(args, answer, credentials):
    job_name = args[0]
    xml = " ".join(args[1:])
    jenk2.create_job(job_name, xml, JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    # server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    # server.create_job(job_name, xml)
    # FIXME
    answer.text = "Создали джобу, но это не точно, проверь сервер"
    return answer


def answer_print_jobs(args, answer, credentials):
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    jobs = server.get_jobs()
    answer.text = 'Описание джоб, которые есть: '+str(jobs)
    return answer


def answer_get_xml_for_job_by_name(args, answer, credentials):
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    job_name = args[0]
    my_job = server.get_job_config(job_name)
    answer.text = 'Xml-конфиг для джобы %s : %s' % (job_name, str(my_job))
    return str(my_job)


def answer_build_job(args, answer, credentials):
    job_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    num = server.build_job(job_name)
    answer.text = 'Джоба сбилджена, номер билда: ' + str(num)
    return answer


def answer_disable_job(args, answer, credentials):
    job_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    server.disable_job(job_name)
    answer.text = 'Джоба %s выключена' % str(job_name)
    return answer


def answer_copy_job(args, answer, credentials):
    job_source_name, new_job_name = args[0:2]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    server.copy_job(job_source_name, new_job_name)
    answer.text = 'Джоба %s скопирована в джобу %s' % (job_source_name, new_job_name)
    return answer


def answer_enable_job(args, answer, credentials):
    job_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    server.enable_job(job_name)
    answer.text = 'Джоба %s включена' % job_name
    return answer


def answer_update_job(args, answer, credentials):
    job_name, new_xml = args[0:2]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    server.reconfig_job(job_name, new_xml)
    answer.text = 'Джоба %s обновлена' % job_name
    return answer


def answer_delete_job(args, answer, credentials):
    job_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    server.delete_job(job_name)
    answer.text = 'Джоба %s удалена' % job_name
    return answer


def answer_get_jobs_from_view(args, answer, credentials):
    view_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    jobs = server.get_jobs(view_name=view_name)
    answer.text = 'Описание джоб, которые есть: ' + str(jobs)
    return answer


def answer_build_parametrized_job(args, answer, credentials):
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    job_name, params_dict = args[0:2]
    #server.build_job('api-test', {'param1': 'test value 1', 'param2': 'test value 2'})
    num = server.build_job(job_name, params_dict)
    answer.text = 'Параметризованная джоба сбилджена, номер билда: ' + str(num)
    return answer


def answer_get_last_completed_build_number(args, answer, credentials):
    job_name = args[0]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
    answer.text = 'Последний успешный номер билда: ' + str(last_build_number)
    return answer


def answer_get_build_info_by_build_number(args, answer, credentials):
    job_name, build_number = args[0:2]
    server = jenkins.Jenkins(JENKINS_SERVER, username=credentials['login'], password=credentials['password'])
    build_info = server.get_build_info(job_name, build_number)
    answer.text = 'Информация о билде номер %s джобы %s: ' % (build_number, job_name) + str(build_info)
    return answer


def answer_get_simple_build_job(args, answer, credentials):
    bitbucket_host, branch_name, bitbucket_login, bitbucket_password, job_name = args[0:5]
    key=randomString(10)
    create_credentials(key, bitbucket_login, bitbucket_password, JENKINS_SERVER, credentials['login'], credentials['password'])
    json = get_credentials_encrypted_token(key, bitbucket_host, JENKINS_SERVER, credentials['login'], credentials['password'])
    xml = create_simple_xml_for_build(bitbucket_host, key, branch_name)
    create_job(job_name, xml, JENKINS_SERVER, credentials['login'], credentials['password'])
    answer.text = 'Построена простая дефолтная джоба %s по билду пулл-реквеста из ветки %s удалённого репозитория %s: ' % (job_name, branch_name, bitbucket_host)
    return answer


def create_credentials(credential_id, bitbucket_host, bitbucket_username, bitbucket_password, host, username, password):
    server = jenkins.Jenkins(JENKINS_SERVER, username=username, password=password)
    table = {
             'credential_id': credential_id,
             'username': bitbucket_username,
             'password': bitbucket_password
             }

    xml = """
    <com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>
        <scope>GLOBAL</scope>
        <id>%(credential_id)s</id>
        <username>%(username)s</username>
        <password>%(password)s</password>
    </com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>
    """ % table
    print(xml)
    server.create_credential(bitbucket_host, xml)

def get_credentials_encrypted_token(credential_id, bitbucket_host, host, username, password):
    server = jenkins.Jenkins(JENKINS_SERVER, username=username, password=password)
    json = server.get_credential_info(credential_id, bitbucket_host)
    print(json)
    return json


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def create_simple_xml_for_build(bitbucket_host, credential_id, branch_name):
    table = {
        'bitbucket_host': bitbucket_host,
        'credential_id': credential_id,
        'branch_name': branch_name
    }
    xml="""
<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@3.12.1">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>%{bitbucket_host}</url>
        <credentialsId>%{credential_id}</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>*/{branch_name}</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers>
    <hudson.triggers.TimerTrigger>
      <spec>H/15 * * * *</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Maven>
      <targets>clean install -P production</targets>
      <mavenName>Maven</mavenName>
      <usePrivateRepository>false</usePrivateRepository>
      <settings class="jenkins.mvn.DefaultSettingsProvider"/>
      <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
      <injectBuildVariables>false</injectBuildVariables>
    </hudson.tasks.Maven>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
    """ % table

    print(xml)

    return xml
