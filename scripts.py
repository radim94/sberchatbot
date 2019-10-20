import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import os
import requests
from utils import read_properties

JENKINS_HOST, BITBUCKET_HOST = read_properties()
print(JENKINS_HOST)
print(BITBUCKET_HOST)

JENKINS_USERNAME = os.environ.get('JENKINS_USERNAME')
JENKINS_PASSWORD = os.environ.get('JENKINS_PASSWORD')

J = Jenkins(JENKINS_HOST, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)

print(J.version)

print(J.keys)

######################################################################################


#from bitbucket.client import Client

BITBUCKET_USER = os.environ.get('BITBUCKET_USER')
BITBUCKET_PASSWORD = os.environ.get('BITBUCKET_PASSWORD')


#client = Client('radim94', '1085607qwertyZ')

#print(client.get_user())

#print(requests.get('http://localhost:7990/rest/api/1.0/users'))

#from bitbucket.bitbucket import Bitbucket

#bb = Bitbucket(BITBUCKET_EMAIL,BITBUCKET_PASSWORD)

#success, repositories = bb.repository.all()

#for repo in repositories:
#    print(repo)


import stashy

stash = stashy.connect(BITBUCKET_HOST, BITBUCKET_USER, BITBUCKET_PASSWORD)

print(stash.admin.users.list())

# FIXME неправильно работает функция чтения пропертей, потом поправить!!!