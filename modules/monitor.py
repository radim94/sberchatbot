import re
from random import random

user_hosts = dict()  # iud, hosts


def answer_host(args, answer, credentials=None):
    if len(args) == 0:
        answer.text = "ERROR"
    else:
        arg_count = len(args) - 1
        uid = args[arg_count]
        hosts = user_hosts.get(uid, [])
        if arg_count == 0:
            # view hosts
            answer.text = "Monitored hosts: {}".format(hosts)
        else:
            cmd = args[0].lower()
            arg_count -= 1  # оставляем аргументы команды
            if cmd == "check":
                if arg_count == 0:
                    answer.text = check_hosts(hosts)
                else:
                    host = args[1]
                    if host.isnumeric():
                        i = int(host)
                        if i < len(hosts):
                            host = hosts[i]
                        else:
                            answer.text = "WRONG HOST INDEX"
                            return
                    answer.text = check_host(host)
            elif cmd == "clear":
                hosts = []
                answer.text = "Hosts cleared"
            elif cmd == "add":
                host = args[1]
                hosts.append(host)
                answer.text = "Host {} added, total host count: {}".format(host, len(hosts))
            else:
                answer.text = "UNKNOWN PARAMS for HOSTS"
        user_hosts[uid] = hosts


def get_host_type(host):
    if host.startswith("http://"):
        return "HTTP"
    elif host.startswith("https://"):
        return "HTTPS"
    elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host):
        return "IP"
    else:
        return "HOST_NAME"


def check_host(host):
    host_type = get_host_type(host)
    if random() * 2 < 1:
        res = "ok"
    else:
        res = "FAILED HOST"
    return "({}) {}: {}".format(host_type, res, host)


def check_hosts(hosts):
    return "\n".join(check_host(host) for host in hosts)
