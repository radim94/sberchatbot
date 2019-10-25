class Alert(object):
    """
        Prometheus AlertMessage
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)


    def __repr__(self):
        return self.get_text_message()

    def __str__(self):
        return self.get_text_message()

    def get_text_message(self):
        return self.activeAt.split(".")[0] + " - " + self.annotations.get("summary", self.annotations.get("description", ""))
