import jenkins # pip install python-jenkins

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



