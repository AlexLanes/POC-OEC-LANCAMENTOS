# std
from dataclasses import dataclass
from typing import TypeAlias, Literal


email: TypeAlias = str
caminhoRelativo: TypeAlias = str
caminhoAbsoluto: TypeAlias = str


__all__ = [
    "email",
    "caminhoAbsoluto",
    "caminhoRelativo"
]