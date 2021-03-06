from typing import Optional

access_token: str
api_version: str
public: int
log_file: str
db_uri: str
stdout_log: Optional[bool] = True
root_dir: Optional[str] = None


def read():
    import dataclasses
    import json

    from .model import Conf
    from .utils import get_settings_path, root_directory

    with open(get_settings_path(), 'r') as _settings:
        _settings = json.load(_settings)
    config = Conf.schema().load(_settings)
    config.root_dir = root_directory()
    for k in dataclasses.asdict(config).keys():
        v = getattr(config, k)
        globals()[k] = v


read()
del globals()['read']
