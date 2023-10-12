# std
from time import sleep
# interno
from src.util import *
from src.tipos import *
from src.logger import *
from src.windows import *
from src.navegador import *
from src.planilhas import *

CAMINHO_EXCEL = rf"{ info_stack().caminho }\documentos\DADOS LANÇAMENTOS.xlsx"
SITE_EBS = "https://o2qa.odebrecht.com"
USUARIO = "dclick"
SENHA = "senha123"

def efetuar_login(navegador: Navegador):
    """Efetuar o login no `SITE_EBS` e esperar a página Home carregar"""
    Logger.informar("Efetuando o login")
    navegador.pesquisar(SITE_EBS)
    navegador.aguardar(
        lambda: Localizadores.texto_login.value.lower() in navegador.driver.title.lower(), 
        f"Texto '{ Localizadores.texto_login.value }' não encontrado no título do navegador"
    )
    # usuario
    elemento = navegador.encontrar("css selector", Localizadores.usuario.value)
    assert elemento != None, "Campo do usuario não encontrado"
    elemento.send_keys(USUARIO)
    # senha
    elemento = navegador.encontrar("css selector", Localizadores.senha.value)
    assert elemento != None, "Campo de senha não encontrado"
    elemento.send_keys(SENHA)
    # efetuar login
    elemento = navegador.encontrar("css selector", Localizadores.efetuar_login.value)
    assert elemento != None, "Botão para efetuar login não encontrado"
    elemento.click()
    # aguardar a pagina 'Home' carregar
    navegador.aguardar(
        lambda: Localizadores.texto_home.value.lower() in navegador.titulo.lower(), 
        f"Texto '{ Localizadores.texto_home.value }' não encontrado no título do navegador"
    )
    Logger.informar("Login efetuado e Home Page carregada")

def main():
    """Fluxo principal"""
    dadosLancamentos = parse_dados_lancamentos(CAMINHO_EXCEL)

    try:
        # abrir navegador no modo Internet Explorer
        with Navegador() as navegador:
            # maximizar janela do navegador
            # efetuar login no `SITE_EBS`
            janelaNavegador = Windows.janela_focada()
            janelaNavegador.maximizar()
            efetuar_login(navegador)
    
    except (TimeoutException, TimeoutError) as erro:
        Logger.erro(f"Erro de timeout na espera de alguma condição/elemento/janela: { erro }")
        exit(1)
    except AssertionError as erro:
        Logger.erro(f"Erro de validação pré-execução de algum passo no fluxo: { erro }")
        exit(1)
    except Exception as erro:
        Logger.erro(f"Erro inesperado no fluxo: { erro }")
        exit(1)
    
if __name__ == "__main__":
    Logger.informar("### Iniciado execução do fluxo ###")
    main()
    Logger.informar("### Finalizado execução com sucesso ###")