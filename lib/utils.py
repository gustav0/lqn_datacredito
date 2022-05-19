import json


def pretty_dict(self, **kwargs):
    return json.dumps(self.dict(**kwargs), indent=2)
