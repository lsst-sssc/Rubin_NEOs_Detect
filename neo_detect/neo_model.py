from abc import ABC, abstractmethod
from pathlib import Path

from astropy.io.ascii import InconsistentTableError, ParameterError
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


class Granvik(NEOModel):
    model_name = "GRANVIK"

    def __init__(self, data_root: Path, filename: str = "granvik_5k.txt"):
        super().__init__(data_root, filename)

    def load_table(self, path: Path) -> Table:
        # Use Astropy's ascii reader and allow comment lines; many Granvik
        # orbit files are whitespace-delimited and may include header/comments.
        try:
            table = Table.read(path, format="ascii", comment="#")
        except (InconsistentTableError, ParameterError):
            # Fallback: read as basic whitespace-delimited ASCII
            table = Table.read(path, format="ascii.basic", delimiter=r"\s+")

        return table

