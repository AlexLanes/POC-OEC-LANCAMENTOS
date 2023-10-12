# std
from enum import Enum, unique
from dataclasses import dataclass
from typing import TypeAlias, Literal


email: TypeAlias = str
caminhoRelativo: TypeAlias = str
caminhoAbsoluto: TypeAlias = str


@unique
class Localizadores(Enum):
    recurso = "a#N55"
    texto_login = "Login"
    departamento = "a#N61"
    texto_home = "Home Page"
    senha = "input#passwordField"
    usuario = "input#usernameField"
    navegacao_dclick = "a#AppsNavLink"
    efetuar_login = "button#SubmitButton"
    texto_aplicativo_oracle = "Aplicativos Oracle"


@dataclass
class Material:
    operacao: str
    item: str
    qtd: str
    motivoAplicacao: str

@dataclass
class OrdemServico:
    os: str
    obra: str
    equipamento: str
    dataInicial: str
    dataTermino: str
    descricao: str
    departamento: str
    atividade: str
    status: str
    tipoOrdemServico: str
    tipoDesativacao: str
    prioridade: str


class DadoLancamento:
    Ordem: OrdemServico
    Materiais: list[Material]
    
    def __init__(self, d: tuple) -> None:
        self.Ordem = OrdemServico(
            d.os, d.obra, d.equipamento, d.data_inicial_programacao, d.data_termino_programacao, d.descricao, 
            d.departamento, d.atividade, d.status, d.tipo_ordem_de_servico, d.tipo_desativacao, d.prioridade
        )
        self.Materiais = [ Material(d.operacao, d.item, d.qtd, d.motivo_aplicacao) ]
    
    @property
    def __dict__(self) -> dict:
        return {
            "Ordem": self.Ordem.__dict__,
            "Materiais": [material.__dict__ for material in self.Materiais]
        }
    
    def __eq__(self, other) -> bool:
        return self.Ordem.__dict__ == other.Ordem.__dict__

    def __str__(self) -> str:
        return self.__dict__.__str__()


__all__ = [
    "email",
    "Material",
    "OrdemServico",
    "Localizadores",
    "DadoLancamento",
    "caminhoAbsoluto",
    "caminhoRelativo"
]