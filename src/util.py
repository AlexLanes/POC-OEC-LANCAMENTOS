# std
import re
from json import dumps
from inspect import stack
from unicodedata import normalize
from multiprocessing.pool import ThreadPool
# interno
from src.tipos import *
# externo
from pandas import DataFrame, ExcelWriter
from xlsxwriter.worksheet import Worksheet

def timeout(segundos: float):
    """Decorator\n-\nExecutar a função por `segundos` segundos até retornar ou `TimeoutError`"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return ThreadPool(1).apply_async(func, args, kwargs).get(segundos) 
        return wrapper
    return decorator

def remover_acentuacao(string: str) -> str:
    """Remover a acentuação de uma string"""
    nfkd = normalize('NFKD', string)
    ascii = nfkd.encode('ASCII', 'ignore')
    return ascii.decode("utf8")

def normalizar(string: str) -> str:
    """Strip, lower, replace espaços por underline e remoção de acentuação"""
    return remover_acentuacao( string.strip().replace(" ", "_").lower() )

def mapear_dtypes(df: DataFrame) -> dict:
    """Criar um dicionário { coluna: tipo } de um dataframe"""
    mapa = {}
    for colunaTipo in df.dtypes.to_string().split("\n"):
        coluna, tipo, *_ = re.split(r"\s+", colunaTipo)
        mapa[coluna] = tipo
    return mapa

def ajustar_colunas(excel: ExcelWriter) -> None:
    """Ajustar a largura das colunas de todas as planilhas no excel"""
    for nomePlanilha in excel.sheets:
        planilha: Worksheet = excel.sheets[nomePlanilha]
        planilha.autofit()

def info_stack(index = 1) -> Arquivo:
    """Obter informações presente no stack dos callers.\n
    - Padrão = Arquivo que chamou o info_stack()"""
    linha = stack()[index].lineno
    funcao = stack()[index].function
    filename = stack()[index].filename
    nome = filename[filename.rfind("\\") + 1 : ]
    caminho = filename[0 : filename.rfind("\\")]
    return Arquivo(nome, caminho, funcao, linha)

def to_json(item) -> str:
    """Retorna o `item` na forma de JSON"""
    return dumps(
        item, ensure_ascii=False, indent=4,
        default=lambda objeto: objeto.__dict__ if hasattr(objeto, "__init__") else objeto
    )

__all__ = [
    "to_json",
    "normalizar",
    "info_stack",
    "mapear_dtypes",
    "ajustar_colunas",
    "remover_acentuacao"
]