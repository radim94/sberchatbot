import json

import json


class Alert(object):
    """
        Prometheus AlertMessage
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def get_text_message(self):
        return self.annotations.get("summary", self.annotations.get("description", ""))

alertd = {
    "status": "firing",
    "labels": {
        "alertname": "DiskSpace70%Free",
        "device": "/dev/sda2",
        "fstype": "ext4",
        "instance": "localhost:9100",
        "job": "node",
        "mountpoint": "/",
        "severity": "Warning"
    },
    "annotations": {
        "description": "localhost:9100  has only 0.6754930465486997% free.",
        "summary": "Instance1 localhost:9100 is low on disk space"
    },
    "startsAt": "2019-10-24T08:12:17.832992086Z",
    "endsAt": "0001-01-01T00:00:00Z",
    "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
    "fingerprint": "7671fb50eef06974"
}

# test = {
#   "receiver": "alertmanager-bot",
#   "status": "firing",
#   "alerts": [
#     {
#       "status": "firing",
#       "labels": {
#         "alertname": "DiskSpace70%Free",
#         "device": "/dev/sda2",
#         "fstype": "ext4",
#         "instance": "localhost:9100",
#         "job": "node",
#         "mountpoint": "/",
#         "severity": "Warning"
#       },
#       "annotations": {
#         "description": "localhost:9100  has only 0.6754930465486997% free.",
#         "summary": "Instance1 localhost:9100 is low on disk space"
#       },
#       "startsAt": "2019-10-24T08:12:17.832992086Z",
#       "endsAt": "0001-01-01T00:00:00Z",
#       "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
#       "fingerprint": "7671fb50eef06974"
#     },
#     {
#       "status": "firing",
#       "labels": {
#         "alertname": "DiskSpace70%Free",
#         "device": "/dev/sdb1",
#         "fstype": "ext4",
#         "instance": "localhost:9100",
#         "job": "node",
#         "mountpoint": "/home",
#         "severity": "Warning"
#       },
#       "annotations": {
#         "description": "localhost:9100  has only 0.6754930465486997% free.",
#         "summary": "Instance1 localhost:9100 is low on disk space"
#       },
#       "startsAt": "2019-10-24T08:12:17.832992086Z",
#       "endsAt": "0001-01-01T00:00:00Z",
#       "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
#       "fingerprint": "015af2a0aed31bdd"
#     },
#     {
#       "status": "firing",
#       "labels": {
#         "alertname": "DiskSpace70%Free",
#         "device": "tmpfs",
#         "fstype": "tmpfs",
#         "instance": "localhost:9100",
#         "job": "node",
#         "mountpoint": "/tmp",
#         "severity": "Warning"
#       },
#       "annotations": {
#         "description": "localhost:9100  has only 0.6754930465486997% free.",
#         "summary": "Instance1 localhost:9100 is low on disk space"
#       },
#       "startsAt": "2019-10-24T08:12:17.832992086Z",
#       "endsAt": "0001-01-01T00:00:00Z",
#       "generatorURL": "http://localhost.localdomain:9090/graph?g0.expr=%28%28node_filesystem_free_bytes%7Bjob%3D%22node%22%7D+%2F+node_filesystem_size_bytes%7Bjob%3D%22node%22%7D%29%29+%3C%3D+1&g0.tab=1",
#       "fingerprint": "3ab5689ce17b14bb"
#     }
#   ],
#   "groupLabels": {
#     "alertname": "DiskSpace70%Free"
#   },
#   "commonLabels": {
#     "alertname": "DiskSpace70%Free",
#     "instance": "localhost:9100",
#     "job": "node",
#     "severity": "Warning"
#   },
#   "commonAnnotations": {
#     "description": "localhost:9100  has only 0.6754930465486997% free.",
#     "summary": "Instance1 localhost:9100 is low on disk space"
#   },
#   "externalURL": "http://localhost.localdomain:9093",
#   "version": "4",
#   "groupKey": "{}:{alertname="DiskSpace70%Free"}"
# }

if __name__ == "__main__":
    # with open('/home/asavt/WORK/sberchatbot/alerts.json') as json_file:
    #     data = json.load(json_file)

    a = Alert(**alertd)
    print(a)
