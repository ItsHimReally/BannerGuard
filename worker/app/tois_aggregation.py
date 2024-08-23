from typing import Any, Optional
import json
import pathlib
import dataclasses

from . import types


@dataclasses.dataclass
class Toi:
    num: int
    size: types.Size
    ids: list[int]


class ToisAggregation:
    def __init__(self, base_path: pathlib.Path) -> None:
        self._base_path = base_path

        self.boards = self._get_boards()
        self.tois = self._get_tois()
        self.toi_nums = [t.num for t in self.tois]
        self.content_ids = self._get_content_ids()

    def _get_boards(self) -> list[dict[str, Any]]:
        path = self._base_path / "BoardsCorrect.json"
        boards: list[dict[str, Any]]
        with open(path, "r", encoding="utf-8") as f:
            boards = json.load(f)

        return boards

    def _check_content_exists(self, content_id: int, size: types.Size) -> bool:
        content_path = self._base_path / f"hackaton/AsiuddContent/{content_id}"
        if not content_path.exists():
            return False

        content_files = list(content_path.iterdir())
        return any([str(size) in f.name for f in content_files])

    def _check_toi_exists(self, num: int) -> bool:
        toi_old_path = self._base_path / f"hackaton/RealTime/{num}"
        toi_new_path = self._base_path / f"toi/{num}"
        toi_old_exists = toi_old_path.exists()
        toi_new_exists = toi_new_path.exists()
        toi_old_path /= "RealTime"
        toi_new_path /= "RealTime"

        if not (toi_old_exists or toi_new_exists):
            return False

        if toi_old_exists:
            if any(toi_old_path.iterdir()):
                return True

        if toi_new_exists:
            if any(toi_new_path.iterdir()):
                return True

        return False

    def _get_tois(self) -> list[Toi]:
        tois: list[Toi] = []

        for el in self.boards:
            num: int = int(el["Num"])

            if not self._check_toi_exists(num):
                continue

            size = types.Size["_" + el["Size"]]
            _ids = [c["id"] for c in el["Content"]["activeContent"]]
            ids = list(filter(lambda id: self._check_content_exists(id, size), _ids))

            if not ids:
                continue

            toi = Toi(
                num=num,
                size=size,
                ids=ids,
            )
            tois += [toi]

        return tois
    
    def get_toi(self, num: int) -> Optional[Toi]:
        toi = [t for t in self.tois if t.num == num]
        if not toi:
            return None
        return toi[0]

    def get_toi_files(self, num: int) -> list[pathlib.Path]:
        if not self._check_toi_exists(num):
            return []

        toi_old_path = self._base_path / f"hackaton/RealTime/{num}"
        toi_new_path = self._base_path / f"toi/{num}"
        toi_old_exists = toi_old_path.exists()
        toi_new_exists = toi_new_path.exists()
        toi_old_path /= "RealTime"
        toi_new_path /= "RealTime"

        paths = []
        if toi_old_exists:
            paths += list(toi_old_path.iterdir())

        if toi_new_exists:
            paths += list(toi_new_path.iterdir())

        return paths
    
    def _get_content_ids(self) -> list[int]:
        contents = self._base_path / "hackaton/AsiuddContent"
        content_ids = sorted(
            [int(c.name) for c in contents.iterdir()],
        )
        return content_ids
        
    def get_content_files(self, content_id: int, size: types.Size) -> list[pathlib.Path]:
        if not self._check_content_exists(content_id, size):
            return []
        
        content_path = self._base_path / f"hackaton/AsiuddContent/{content_id}"
        content_files = [f for f in content_path.iterdir() if str(size) in f.name]
        return content_files
