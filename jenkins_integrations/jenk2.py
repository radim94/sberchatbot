import jenkins # pip install python-jenkins
import uuid

def hello_user(host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))


def get_jobs_count(host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    return server.jobs_count()

def create_job(job_name, xml, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.create_job(job_name, xml)

def print_jobs(host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    jobs = server.get_jobs()
    print(jobs)

def get_xml_for_job_by_name(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    my_job = server.get_job_config(job_name)
    return str(my_job)


def build_job(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.build_job(job_name)


def disable_job(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.disable_job(job_name)


def copy_job(job_source_name, new_job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.copy_job(job_source_name, new_job_name)


def enable_job(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.enable_job(job_name)

def update_job(job_name, new_xml, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.reconfig_job(job_name, new_xml)


def delete_job(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    server.delete_job(job_name)


def get_jobs_from_view(view_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    jobs = server.get_jobs(view_name=view_name)
    return jobs



# build a parameterized job
# requires creating and configuring the api-test job to accept 'param1' & 'param2'
def build_parametrized_job(job_name, params_dict, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    #server.build_job('api-test', {'param1': 'test value 1', 'param2': 'test value 2'})
    server.build_job(job_name, params_dict)

def get_last_completed_build_number(job_name, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
    return last_build_number

def get_build_info_by_build_number(job_name, build_number, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
    build_info = server.get_build_info(job_name, build_number)
    return build_info

def create_credentials(credential_id, bitbucket_host, bitbucket_username, bitbucket_password, host, username, password):
    server = jenkins.Jenkins(host, username=username, password=password)
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
    server = jenkins.Jenkins(host, username=username, password=password)
    json = server.get_credential_info(credential_id, bitbucket_host)
    print(json)
    return json

'''
from utils import read_properties
import os

JENKINS_HOST, BITBUCKET_HOST = read_properties()
print(JENKINS_HOST)
print(BITBUCKET_HOST)

JENKINS_USERNAME = os.environ.get('JENKINS_USERNAME')
JENKINS_PASSWORD = os.environ.get('JENKINS_PASSWORD')
BITBUCKET_USERNAME = os.environ.get('BITBUCKET_USER')
BITBUCKET_PASSWORD = os.environ.get('BITBUCKET_PASSWORD')'''


import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_simple_build_job(bitbucket_host, branch_name, bitbucket_login, bitbucket_password, job_name, jenkins_host, jenkins_username, jenkins_password):
    key=randomString(10)
    create_credentials(key,bitbucket_login, bitbucket_password,jenkins_host, jenkins_username, jenkins_password)
    json = get_credentials_encrypted_token(key, bitbucket_host, jenkins_host, jenkins_username, jenkins_password)
    xml = create_simple_xml_for_build(bitbucket_host, key, branch_name)
    create_job(job_name, xml, jenkins_host, jenkins_username, jenkins_password)




#create_credentials('165', 'Test Folder', BITBUCKET_USERNAME, BITBUCKET_PASSWORD, JENKINS_HOST, JENKINS_USERNAME, JENKINS_PASSWORD)

#json=get_credentials_encrypted_token('165', BITBUCKET_HOST, JENKINS_HOST, JENKINS_USERNAME, JENKINS_PASSWORD)

#'http://user:token@jenkins_server:8080/credentials/store/system/domain/_/createCredentials'

#http://localhost:8080/job/http%3A/job/job/localhost%3A7990/credentials/store/folder/domain/global/createCredentials

#'http://localhost:8080/credentials/store/system/domain/_/createCredentials'

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




