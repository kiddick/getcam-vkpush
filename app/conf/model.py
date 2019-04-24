from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


class LightWeightToDictMixin:

    def as_dict(self):
        return self.__dict__


@dataclass_json
@dataclass
class Conf:
    # here is should be same content as in __init__.py
    access_token: str
    api_version: str
    public: int
    log_file: str
    db_uri: str
    stdout_log: Optional[bool] = True
    root_dir: Optional[str] = None
