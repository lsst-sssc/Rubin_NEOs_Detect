from abc import ABC, abstractmethod
from pathlib import Path

from astropy.table import Table


class NEOModel(ABC):
    model_name: str

    def __init__(self, data_root: Path, filename: str):
        self.data_root = data_root
        self.filename = filename
        self._neo_table = None

    @property
    def path(self) -> Path:
        return self.data_root / self.filename

    @property
    def neo_table(self) -> Table:
        if self._neo_table is None:
            self._neo_table = self.load_table(self.path)
        return self._neo_table

    @abstractmethod
    def load_table(self, path: Path) -> Table:
        raise NotImplementedError


class NEOMOD3(NEOModel):
    model_name = "NEOMOD3"

    def __init__(self, data_root: Path, filename: str = "output_file.txt"):
        super().__init__(data_root, filename)

    def load_table(self, path: Path) -> Table:
        return Table.read(
            path,
            format="ascii",
            names=["H", "a", "e", "inc", "diam", "pV"],
        )

