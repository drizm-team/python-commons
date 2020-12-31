import pathlib
from typing import Optional

class Path(pathlib.Path):
    def rmdir(self, recursive: Optional[bool] = True) -> None: ...
