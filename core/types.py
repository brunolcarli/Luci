import json
from typing import Optional, DefaultDict, Dict
from collections import defaultdict


class CompressedDict:
    """
    Comprime um dicionário em formato binário para armazenamento robusto.
    """
    def __init__(self, data: Dict[str, int]) -> None:
        self._compress(data)

    def _compress(self, data: Dict[str, int]) -> None:
        self.bit_string = json.dumps(data).encode('utf-8')

    def decompress(self) -> DefaultDict[str, int]:
        return json.loads(self.bit_string.decode('utf-8'))

    @staticmethod
    def decompress_bytes(bit_string: bytes) -> Dict[str, int]:
        data = json.loads(bit_string.decode('utf-8')) if bit_string else {}
        return defaultdict(int, data)

    def __repr__(self) -> str:
        return repr(self.decompress())

    def __getitem__(self, key: str) -> Optional:
        return self.decompress().get(key)