from pathlib import Path

from clld.web.assets import environment

import dorelld


environment.append_path(
    Path(dorelld.__file__).parent.joinpath('static').as_posix(),
    url='/dorelld:static/')
environment.load_path = list(reversed(environment.load_path))
