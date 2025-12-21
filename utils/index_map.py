# utils/index_map.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class IndexMap:
    ids: List[str]              # index -> id
    id2index: Dict[str, int]    # id -> index

    @classmethod
    def from_locations(cls, locations: List[Any]):
        ids = [loc.id for loc in locations]
        return cls(ids=ids, id2index={id_: i for i, id_ in enumerate(ids)})

    def idx(self, id_: str) -> int:
        return self.id2index[id_]

    def id(self, idx: int) -> str:
        return self.ids[idx]
