# std
from dataclasses import dataclass
# interno
from src.util import *
from src.tipos import *
from src.logger import *
# externo
from pandas import read_excel


def parse_dados_lancamentos(caminho: caminhoAbsoluto) -> list[DadoLancamento]:
    """Realiza o parse da planilha recursos do excel, com base no caminho absoluto, para um formato amigável"""
    NOME_PLANILHA = "APONTAMENTO_OS"
    COLUNAS_TIPOS_ESPERADOS = {
        "os": "object",
        "obra": "object",
        "equipamento": "object",
        "data_inicial_programacao": "object",
        "data_termino_programacao": "object",
        "descricao": "object",
        "departamento": "object",
        "atividade": "object",
        "status": "object",
        "tipo_ordem_de_servico": "object",
        "tipo_desativacao": "object",
        "prioridade": "object",
        "operacao": "object",
        "item": "object",
        "qtd": "object",
        "motivo_aplicacao": "object"
    }

    Logger.informar(f"Iniciado o parse da planilha '{NOME_PLANILHA}'")
    try:
        # ler e criar dataframe 
        # tratar nome das colunas
        df = read_excel(caminho, sheet_name=NOME_PLANILHA, keep_default_na=False, date_format="%Y-%M-%D")
        df.columns = df.columns.to_series().apply(normalizar)

        # validação das colunas do dataframe
        colunasDf = list( mapear_dtypes(df).keys() )
        colunasEsperadas = list( COLUNAS_TIPOS_ESPERADOS.keys() )
        assert sorted(colunasEsperadas) == sorted(colunasDf), f"Nome(s) de coluna inesperado \n\tesperado {colunasEsperadas} \n\trecebido {colunasDf}"
        
        # order by, de `os` até `prioridade`, para as linhas iguais ficarem sequenciais
        df.sort_values( by=colunasEsperadas[0:12], inplace=True )
        
        # conversão para str dos campos possivelmente numéricos/dateTime
        df["qtd"] = df["qtd"].astype(str)
        df["item"] = df["item"].astype(str)
        df["operacao"] = df["operacao"].astype(str)
        df["atividade"] = df["atividade"].astype(str)
        df["motivo_aplicacao"] = df["motivo_aplicacao"].astype(str)
        df["data_inicial_programacao"] = df["data_inicial_programacao"].dt.strftime("%d-%b-%Y %H:%M:%S")
        df["data_termino_programacao"] = df["data_termino_programacao"].dt.strftime("%d-%b-%Y %H:%M:%S")

        # validação dos tipos do dataframe
        tiposDf = list( mapear_dtypes(df).values() )
        tiposEsperados = list( COLUNAS_TIPOS_ESPERADOS.values() )
        assert sorted(tiposEsperados) == sorted(tiposDf), f"Tipo(s) de coluna inesperado \n\tesperado {tiposEsperados} \n\trecebido {tiposDf}"

        # criar a lista de dados de Lancamentos
        # agregar os dados de Lancamentos iguais
        dadosLancamentos: list[DadoLancamento] = []
        for item in df.itertuples(index=False):
            item = DadoLancamento(item)
            if len(dadosLancamentos) == 0: del df # salvar memoria
            if len(dadosLancamentos) > 0 and item == dadosLancamentos[-1]:
                dadosLancamentos[-1].Materiais.extend(item.Materiais)
            else: dadosLancamentos.append(item)
        
        Logger.informar(f"Finalizado o parse da planilha '{NOME_PLANILHA}'")
        return dadosLancamentos

    except FileNotFoundError:
        Logger.erro(f"Excel não encontrado em '{caminho}'")
        exit(1)
    except AssertionError as erro:
        Logger.erro(f"Falha de validação da planilha '{NOME_PLANILHA}': {erro}")
        exit(1)
    except Exception as erro:
        Logger.erro(f"Erro inesperado na leitura da planilha '{NOME_PLANILHA}': {erro}")
        exit(1)


__all__ = [
    "parse_dados_lancamentos"
]