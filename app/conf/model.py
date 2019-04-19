from dataclasses import dataclass

from dataclasses_json import dataclass_json


class LightWeightToDictMixin:

    def as_dict(self):
        return self.__dict__


@dataclass_json
@dataclass
class Conf:
    # here is should be same content as in __init__.py
    test: str
